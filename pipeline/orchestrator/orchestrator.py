"""Оркестратор: последовательный проход по этапам пайплайна.

Один этап = один агент = один артефакт. Артефакты предыдущих этапов
передаются следующим агентам через ``inputs``. Question Gate останавливает
прогон при blocking-вопросах до появления ``answers.json``.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pipeline.agents.architecture_api import ArchitectureApiAgent
from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.agents.codegen_backend import CodegenBackendAgent
from pipeline.agents.codegen_frontend import CodegenFrontendAgent
from pipeline.agents.docs_agent import DocsAgent
from pipeline.agents.requirements import RequirementsAgent
from pipeline.agents.security_agent import SecurityReportAgent
from pipeline.agents.system_analysis import SystemAnalysisAgent
from pipeline.agents.tests_agent import TestsAgent
from pipeline.agents.ui import UiDesignAgent
from pipeline.config import Settings
from pipeline.errors import StageFailed
from pipeline.llm.client import LLMClient
from pipeline.orchestrator.state import RunState

logger = logging.getLogger(__name__)

# Порядок этапов: (имя этапа, класс агента).
STAGES: list[tuple[str, type[BaseAgent]]] = [
    ("01_requirements", RequirementsAgent),
    ("02_system_analysis", SystemAnalysisAgent),
    ("03_architecture_api", ArchitectureApiAgent),
    ("04_ui_design", UiDesignAgent),
    ("05_codegen_backend", CodegenBackendAgent),
    ("06_codegen_frontend", CodegenFrontendAgent),
    ("07_tests", TestsAgent),
    ("08_security_report", SecurityReportAgent),
    ("09_docs", DocsAgent),
]


def _read_json(path: Path) -> dict[str, Any]:
    """Прочитать JSON-артефакт с диска.

    Args:
        path: Путь к JSON-файлу.

    Returns:
        Словарь или пустой dict, если файла нет.
    """
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _build_inputs(run_dir: Path, initial: dict[str, Any]) -> dict[str, Any]:
    """Собрать входные данные этапов из сохранённых артефактов.

    Args:
        run_dir: Корень прогона.
        initial: Начальные входы (requirements_md, answers, case_dir).

    Returns:
        Словарь inputs для агентов: requirements, system_analysis,
        architecture, ui.
    """
    inputs: dict[str, Any] = dict(initial)
    req = _read_json(run_dir / "01_requirements" / "requirements.json")
    if req:
        inputs["requirements"] = req
    # system-analysis.md — markdown; системную модель как JSON держим
    # в requirements.json (roles) и в system-model.json (если появится).
    sm = _read_json(run_dir / "02_system_analysis" / "system-model.json")
    if sm:
        inputs["system_analysis"] = sm
    arch_full = _read_json(run_dir / "03_architecture_api" / "architecture.json")
    if arch_full:
        inputs["architecture"] = arch_full
    # OpenAPI (для codegen backend).
    import yaml

    openapi_path = run_dir / "03_architecture_api" / "openapi.yaml"
    if openapi_path.exists():
        try:
            inputs["openapi"] = yaml.safe_load(openapi_path.read_text(encoding="utf-8")) or {}
        except Exception:  # noqa: BLE001
            inputs["openapi"] = {}
    # ui-spec (для codegen frontend).
    ui_path = run_dir / "04_ui_design" / "ui-spec.json"
    ui = _read_json(ui_path)
    if ui:
        inputs["ui_spec"] = ui
    return inputs


def _persist_artifacts(stage_dir: Path, artifacts: dict[str, Any]) -> None:
    """Записать артефакты этапа на диск.

    Args:
        stage_dir: Директория этапа (``generated/<case>/{stage}/``).
        artifacts: Словарь «имя файла -> содержимое».
    """
    stage_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in artifacts.items():
        path = stage_dir / filename
        if isinstance(content, (dict, list)):
            path.write_text(
                json.dumps(content, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        else:
            path.write_text(str(content), encoding="utf-8")


def run_pipeline(
    run_dir: Path,
    requirements_md: str,
    answers: dict[str, str] | None = None,
    settings: Settings | None = None,
) -> str:
    """Выполнить все этапы пайплайна.

    Args:
        run_dir: Корень прогона (``generated/<case>/``).
        requirements_md: Текст бизнес-требований.
        answers: Ответы на blocking-вопросы (``{question_id: answer}``).
        settings: Конфигурация LLM (по умолчанию — из env).

    Returns:
        ``"done"`` при полном завершении, ``"waiting_answers"`` при
        остановке на blocking-вопросах.

    Raises:
        StageFailed: Если этап упал (исключение или непройденные gates).
    """
    settings = settings or Settings()
    state = RunState(run_dir)
    llm = LLMClient(run_dir, settings)

    initial: dict[str, Any] = {
        "requirements_md": requirements_md,
        "answers": answers or {},
    }

    for stage_name, agent_cls in STAGES:
        if state.stage_status(stage_name) == "done":
            logger.info("Этап %s уже завершён — пропуск", stage_name)
            continue

        state.start_stage(stage_name, agent_cls.prompt_version)
        agent = agent_cls(llm, run_dir)

        inputs = _build_inputs(run_dir, initial)
        try:
            result: AgentResult = agent.run(inputs)
        except Exception as exc:  # noqa: BLE001
            state.fail_stage(stage_name, str(exc))
            raise StageFailed(f"Этап {stage_name!r} упал: {exc}") from exc

        # Question Gate: blocking-вопросы останавливают прогон.
        if result.questions_blocking > 0:
            state.wait_answers(stage_name)
            return "waiting_answers"

        # Persist артефактов.
        _persist_artifacts(run_dir / stage_name, result.artifacts)
        state.finish_stage(stage_name, result.gates)

    return "done"
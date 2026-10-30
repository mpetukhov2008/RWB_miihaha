"""Оркестратор: последовательный проход по этапам пайплайна.

Один этап = один агент = один артефакт. После каждого агента проверяется
Question Gate: если в артефакте есть blocking-вопросы — прогон останавливается
и ждёт ``answers.json``. Артефакты персистятся в ``runs/{id}/{stage}/``.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.agents.requirements import RequirementsAgent
from pipeline.config import Settings
from pipeline.errors import StageFailed
from pipeline.llm.client import LLMClient
from pipeline.pipeline.state import RunState

logger = logging.getLogger(__name__)

# Порядок этапов: (имя, класс агента).
STAGES: list[tuple[str, type[BaseAgent]]] = [
    ("requirements", RequirementsAgent),
]


def _persist_artifacts(stage_dir: Path, artifacts: dict[str, Any]) -> None:
    """Записать артефакты этапа на диск.

    Args:
        stage_dir: Директория этапа (``runs/{id}/{stage}/``).
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
        run_dir: Корень прогона (``runs/{run_id}/``).
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

    inputs: dict[str, Any] = {
        "requirements_md": requirements_md,
        "answers": answers or {},
    }

    for stage_name, agent_cls in STAGES:
        if state.stage_status(stage_name) == "done":
            logger.info("Этап %s уже завершён — пропуск", stage_name)
            continue

        state.start_stage(stage_name, agent_cls.prompt_version)
        agent = agent_cls(llm, run_dir)
        try:
            result: AgentResult = agent.run(inputs)
        except Exception as exc:  # noqa: BLE001
            state.fail_stage(stage_name, str(exc))
            raise StageFailed(f"Этап {stage_name!r} упал: {exc}") from exc

        # Question Gate: блокирующие вопросы останавливают прогон.
        if result.questions_blocking > 0:
            state.wait_answers(stage_name)
            return "waiting_answers"

        # Persist артефактов.
        _persist_artifacts(run_dir / stage_name, result.artifacts)
        state.finish_stage(stage_name, result.gates)

    return "done"
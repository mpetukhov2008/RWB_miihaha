"""Codegen Frontend-агент: генерирует Angular-каркас из ui-spec.

Детерминированно строит экраны и сервисы; ответ LLM (если есть) может
дополнить компоненты, но каркас строится всегда.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.generators.frontend import build_frontend_skeleton


class CodegenFrontendAgent(BaseAgent[dict[str, Any]]):
    """Агент генерации frontend.

    Attributes:
        name: Имя этапа — ``06_codegen_frontend``.
    """

    name = "06_codegen_frontend"
    prompt_version = "v1"
    _FILE_SCHEMA = {
        "type": "object",
        "required": ["summary", "files"],
        "properties": {
            "summary": {"type": "string"},
            "files": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["path", "content"],
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                },
            },
        },
    }

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema ответа."""
        return self._FILE_SCHEMA

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: ui-spec (урезанный) + operations + схема.

        Каркас строится детерминированно в validate(); от LLM нужны только
        небольшие дополнения, поэтому промпт намеренно ограничен по объёму.
        """
        ui = inputs.get("ui_spec", {}) or {}
        arch = inputs.get("architecture", {}) or {}
        # Урезаем ui-spec: только первые 3 экрана/флоу — этого достаточно,
        # чтобы модель не упиралась в лимит вывода и не обрывала JSON.
        screens = (ui.get("screens") or [])[:3]
        flows = (ui.get("flows") or [])[:2]
        ui_slim = {"flows": flows, "screens": screens}
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Сгенерируй НЕБОЛЬШОЕ дополнение к Angular-каркасу.\n"
            "Правила (строго):\n"
            "- Не более 5 файлов в files.\n"
            "- Каждый файл — не более 80 строк.\n"
            "- Без стилей, без тестов, без конфигов, без package.json.\n"
            "- Только то, что дополняет каркас (компоненты экранов/сервис).\n"
            "- Ответ — ОДИН валидный JSON-объект, обязательно закрой все строки и скобки.\n"
            "- Если не влезаешь — сократи число файлов, но JSON должен быть валидным.\n\n"
            f"=== UI-SPEC (сокращённый) ===\n{json.dumps(ui_slim, ensure_ascii=False)}\n\n"
            f"=== OPERATIONS (первые 10) ===\n{json.dumps((arch.get('operations') or [])[:10], ensure_ascii=False)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ + построить детерминированный каркас.

        Args:
            data: Ответ LLM.
            inputs: Входные данные (ui_spec, architecture).

        Returns:
            AgentResult с файлами frontend.
        """
        llm_files: dict[str, str] = {}
        for f in data.get("files") or []:
            llm_files[f["path"]] = f["content"]

        ui = inputs.get("ui_spec") or {}
        arch = inputs.get("architecture") or {}
        skeleton = build_frontend_skeleton(ui, arch.get("operations") or [])

        files = {**skeleton, **llm_files}

        artifacts: dict[str, Any] = {}
        for path, content in files.items():
            artifacts[f"frontend-admin/{path}"] = content

        gates: dict[str, str] = {
            "schema": "ok",
            "files_nonempty": "ok" if files else "fail",
            "screens_generated": (
                "ok" if any("/screens/" in p for p in files) else "fail"
            ),
        }
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

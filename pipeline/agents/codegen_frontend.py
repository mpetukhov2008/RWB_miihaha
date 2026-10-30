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
        """Собрать user-промпт: ui-spec + operations + схема."""
        ui = inputs.get("ui_spec", {})
        arch = inputs.get("architecture", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — ui-spec. Сгенерируй Angular-файлы.\n\n"
            f"=== UI-SPEC.JSON ===\n{json.dumps(ui, ensure_ascii=False, indent=2)}\n\n"
            f"=== OPERATIONS ===\n{json.dumps(arch.get('operations', []), ensure_ascii=False, indent=2)}\n\n"
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
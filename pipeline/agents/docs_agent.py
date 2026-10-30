"""Docs-агент: генерирует документацию результата.

Принимает от LLM список файлов и валидирует, что README содержит
install/run/test, user-guide покрывает must-FR, известные ограничения
включают assumptions; затем персистит файлы.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent


class DocsAgent(BaseAgent[dict[str, Any]]):
    """Агент документации.

    Attributes:
        name: Имя этапа — ``09_docs``.
    """

    name = "09_docs"
    prompt_version = "v1"
    _SCHEMA = {
        "type": "object",
        "required": ["files"],
        "properties": {
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
            }
        },
    }

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema ответа."""
        return self._SCHEMA

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: requirements + схема."""
        requirements = inputs.get("requirements", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — требования. Сгенерируй документацию.\n\n"
            f"=== REQUIREMENTS.JSON ===\n{json.dumps(requirements, ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать файлы и собрать артефакты.

        Args:
            data: Ответ LLM (files: path/content).
            inputs: Входные данные (requirements).

        Returns:
            AgentResult с документами.
        """
        files: dict[str, str] = {}
        for f in data.get("files") or []:
            files[f["path"]] = f["content"]

        readme = files.get("README.md", "")
        user_guide = files.get("docs/user-guide.md", "")
        limitations = files.get("docs/known-limitations.md", "")

        requirements = inputs.get("requirements", {})
        must_ids = [
            r["id"]
            for r in requirements.get("requirements", [])
            if r.get("priority") == "must"
        ]
        assumptions = requirements.get("assumptions", [])

        gates: dict[str, str] = {
            "schema": "ok",
            "readme_commands": (
                "ok"
                if all(k in readme for k in ("install", "run", "test"))
                else "fail"
            ),
            "user_guide_must": (
                "ok"
                if all(rid in user_guide for rid in must_ids)
                else "fail"
            ),
            "limitations_assumptions": (
                "ok"
                if all(a in limitations for a in assumptions)
                else "fail"
            ),
        }

        artifacts: dict[str, Any] = {}
        for path, content in files.items():
            artifacts[f"docs/{path}"] = content
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

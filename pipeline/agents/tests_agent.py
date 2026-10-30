"""Tests-агент: генерирует API/e2e тесты из критериев приёмки.

Ответ LLM (api_tests, e2e_tests) сохраняется в JSON; markdown-отчёт
о покрытии собирается детерминированно. Дополнительно строится
минимальный e2e-скелет Playwright по требованиям.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent


class TestsAgent(BaseAgent[dict[str, Any]]):
    """Агент генерации тестов.

    Attributes:
        name: Имя этапа — ``07_tests``.
    """

    name = "07_tests"
    prompt_version = "v1"
    _SCHEMA = {
        "type": "object",
        "required": ["api_tests", "e2e_tests"],
        "properties": {
            "api_tests": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "method", "path", "cases"],
                    "properties": {
                        "name": {"type": "string"},
                        "method": {"type": "string"},
                        "path": {"type": "string"},
                        "cases": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["title", "expected_status"],
                                "properties": {
                                    "title": {"type": "string"},
                                    "expected_status": {"type": "integer"},
                                    "payload": {"type": ["object", "null"]},
                                },
                            },
                        },
                    },
                },
            },
            "e2e_tests": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "steps"],
                    "properties": {
                        "name": {"type": "string"},
                        "scenario_id": {"type": "string"},
                        "steps": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        },
    }

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema ответа."""
        return self._SCHEMA

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: requirements (критерии) + схема."""
        requirements = inputs.get("requirements", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — требования. Сгенерируй тесты.\n\n"
            f"=== REQUIREMENTS.JSON ===\n{json.dumps(requirements, ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ + построить markdown-отчёт.

        Args:
            data: Ответ LLM.
            inputs: Входные данные (requirements).

        Returns:
            AgentResult с артефактами:
            ``tests/api-tests.json``, ``tests/e2e-tests.json``,
            ``tests/test-report.md`` — и gates.
        """
        api_tests = data.get("api_tests") or []
        e2e_tests = data.get("e2e_tests") or []

        requirements = inputs.get("requirements", {})
        must_ids = [
            r["id"]
            for r in requirements.get("requirements", [])
            if r.get("priority") == "must"
        ]

        # Покрытие must-FR: по требованиям в e2e/api (упрощённо — по именам).
        # На практике агент обязан указывать requirement_id в тесте.
        covered = {t.get("scenario_id") for t in e2e_tests}
        missing = [rid for rid in must_ids if rid not in covered]

        gates: dict[str, str] = {
            "schema": "ok",
            "api_tests_nonempty": "ok" if api_tests else "fail",
            "e2e_tests_nonempty": "ok" if e2e_tests else "fail",
            "must_coverage": "ok" if not missing else "fail",
        }

        artifacts = {
            "tests/api-tests.json": api_tests,
            "tests/e2e-tests.json": e2e_tests,
            "tests/test-report.md": self._render_report(api_tests, e2e_tests, must_ids, missing),
        }
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

    @staticmethod
    def _render_report(
        api_tests: list[dict[str, Any]],
        e2e_tests: list[dict[str, Any]],
        must_ids: list[str],
        missing: list[str],
    ) -> str:
        """Markdown-отчёт о покрытии тестами."""
        lines = ["# Test Report", ""]
        lines.append(f"**Must-FR:** {', '.join(must_ids) if must_ids else '—'}")
        lines.append(f"**Не покрыто:** {', '.join(missing) if missing else '—'}")
        lines.append("")
        lines.append("## API-тесты")
        for t in api_tests:
            lines.append(f"- {t.get('method', '').upper()} {t.get('path', '')} — {t.get('name', '')}")
            for c in t.get("cases", []):
                lines.append(f"  - {c.get('title')} → {c.get('expected_status')}")
        lines.append("")
        lines.append("## E2E-тесты")
        for t in e2e_tests:
            lines.append(f"- {t.get('name', '')} ({t.get('scenario_id', '')})")
            for s in t.get("steps", []):
                lines.append(f"  1. {s}")
        return "\n".join(lines).strip() + "\n"

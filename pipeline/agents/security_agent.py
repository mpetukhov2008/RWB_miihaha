"""Security Report-агент: отчёт по безопасности.

Принимает от LLM список findings и собирает ``reports/security-report.md``
детерминированно.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent


class SecurityReportAgent(BaseAgent[dict[str, Any]]):
    """Агент отчёта по безопасности.

    Attributes:
        name: Имя этапа — ``08_security_report``.
    """

    name = "08_security_report"
    prompt_version = "v1"
    _SCHEMA = {
        "type": "object",
        "required": ["summary", "findings"],
        "properties": {
            "summary": {"type": "string"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["severity", "title", "description", "status"],
                    "properties": {
                        "severity": {"enum": ["critical", "high", "medium", "low", "info"]},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "status": {"enum": ["open", "mitigated", "not-applicable"]},
                    },
                },
            },
        },
    }

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema ответа."""
        return self._SCHEMA

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: architecture + схема."""
        arch = inputs.get("architecture", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — архитектура. Составь security-отчёт.\n\n"
            f"=== ARCHITECTURE.JSON ===\n{json.dumps(arch, ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ + собрать markdown.

        Args:
            data: ��твет LLM.
            inputs: Входные данные (не используются в gates).

        Returns:
            AgentResult с ``reports/security-report.md``.
        """
        findings = data.get("findings") or []
        gates: dict[str, str] = {
            "schema": "ok",
            "findings_nonempty": "ok" if findings else "fail",
        }

        artifacts = {"reports/security-report.md": self._render(data)}
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

    @staticmethod
    def _render(data: dict[str, Any]) -> str:
        """Markdown-отчёт из данных LLM."""
        lines = ["# Security Report", ""]
        lines.append(data.get("summary", ""))
        lines.append("")
        lines.append("## Findings")
        lines.append("| Severity | Title | Status | Description |")
        lines.append("|---|---|---|---|")
        for f in data.get("findings", []):
            lines.append(
                f"| {f.get('severity')} | {f.get('title')} | {f.get('status')} | {f.get('description')} |"
            )
        return "\n".join(lines).strip() + "\n"
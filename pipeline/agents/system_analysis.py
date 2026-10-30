"""System Analysis-агент: requirements.json -> system-analysis.

Генерирует артефакт ``system-analysis.md`` через детерминированную сборку
markdown из структурированного ответа LLM (SystemAnalysis).
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.schemas.system_model import SystemAnalysis


class SystemAnalysisAgent(BaseAgent[SystemAnalysis]):
    """Агент системного анализа.

    Attributes:
        name: Имя этапа — ``02_system_analysis``.
    """

    name = "02_system_analysis"
    prompt_version = "v1"

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema артефакта системного анализа."""
        return SystemAnalysis.model_json_schema()

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: requirements.json + схема.

        Args:
            inputs: Словарь с ключом ``requirements`` (данные requirements.json).

        Returns:
            Текст user-промпта.
        """
        requirements = inputs.get("requirements", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — артефакт требований. Построй системную модель.\n\n"
            f"=== REQUIREMENTS.JSON ===\n{json.dumps(requirements, ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ: схема + gates.

        Args:
            data: Ответ модели.
            inputs: Входные данные (требования).

        Returns:
            AgentResult с артефактом ``system-analysis.md`` и gates.
        """
        model = SystemAnalysis.model_validate(data)
        markdown = self._render_markdown(model)

        # Простейший gate: сценарии не пусты и акторы есть.
        gates: dict[str, str] = {
            "schema": "ok",
            "scenarios_nonempty": "ok" if model.scenarios else "fail",
            "actors_defined": (
                "ok"
                if all(s.actor for s in model.scenarios)
                else "fail"
            ),
        }

        artifacts = {"system-analysis.md": markdown}
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

    @staticmethod
    def _render_markdown(model: SystemAnalysis) -> str:
        """Собрать markdown-артефакт из модели (детерминированно).

        Args:
            model: Валидная системная модель.

        Returns:
            Текст ``system-analysis.md``.
        """
        lines: list[str] = ["# Системный анализ", ""]
        lines.append("## Границы системы")
        inside = ", ".join(model.boundaries.inside) if model.boundaries.inside else "—"
        outside = ", ".join(model.boundaries.outside) if model.boundaries.outside else "—"
        lines.append(f"**Внутри:** {inside}")
        lines.append(f"**Снаружи:** {outside}")
        lines.append("")
        lines.append("## Роли и разрешения")
        for rp in model.roles_permissions:
            lines.append(f"- **{rp.role}**: " + "; ".join(rp.permissions))
        lines.append("")
        lines.append("## Сценарии использования")
        for s in model.scenarios:
            lines.append(f"### {s.id}: {s.title}")
            lines.append(f"**Актор:** {s.actor}")
            if s.requirement_ids:
                lines.append("**Требования:** " + ", ".join(s.requirement_ids))
            lines.append("**Шаги:**")
            for step in s.steps:
                lines.append(f"1. {step}")
            lines.append(f"**Результат:** {s.result}")
            lines.append("")
        lines.append("## Сущности")
        for e in model.entities:
            lines.append(f"- **{e.name}** — {e.description}")
        lines.append("")
        lines.append("## Допущения")
        for a in model.assumptions:
            lines.append(f"- {a}")
        lines.append("")
        lines.append("## Открытые вопросы")
        for q in model.open_questions:
            lines.append(f"- {q}")
        return "\n".join(lines).strip() + "\n"

"""Requirements-агент: бизнес-требования -> RequirementsDoc.

Генерирует ``requirements.json``: цели, роли, FR/NFR, ограничения, риски,
допущения и открытые вопросы. Проверяет уникальность ID, лимиты вопросов
и критерии приёмки must-требований.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.schemas.requirements import RequirementsDoc


class RequirementsAgent(BaseAgent[RequirementsDoc]):
    """Агент анализа требований.

    Attributes:
        name: Имя этапа — ``requirements``.
        prompt_version: ``v1``.
    """

    name = "requirements"
    prompt_version = "v1"

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema артефакта требований."""
        return RequirementsDoc.model_json_schema()

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: требования + ответы + схема.

        Args:
            inputs: Словарь с ключами ``requirements_md`` (текст требований)
                и ``answers`` (ответы на blocking-вопросы, опционально).

        Returns:
            Текст user-промпта.
        """
        requirements_md = inputs.get("requirements_md", "")
        answers = inputs.get("answers") or {}
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        answers_text = json.dumps(answers, ensure_ascii=False, indent=2) if answers else "нет"

        return (
            "Ниже — бизнес-требования заказчика.\n"
            "Проанализируй их и верни JSON, строго соответствующий схеме.\n\n"
            f"=== БИЗНЕС-ТРЕБОВАНИЯ ===\n{requirements_md}\n\n"
            f"=== ОТВЕТЫ НА BLOCKING-ВОПРОСЫ (если были) ===\n{answers_text}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ: схема + gates.

        Args:
            data: Ответ модели.
            inputs: Входные данные этапа (не используются в gates требований).

        Returns:
            AgentResult с артефактом ``requirements.json`` и gates.
        """
        doc = RequirementsDoc.model_validate(data)

        gates: dict[str, str] = {}
        ids = [r.id for r in doc.requirements]
        gates["schema"] = "ok"
        gates["unique_ids"] = "ok" if len(ids) == len(set(ids)) else "fail"
        gates["questions_limit"] = "ok" if len(doc.open_questions) <= 5 else "fail"
        blocking = [q for q in doc.open_questions if q.severity == "blocking"]
        gates["blocking_limit"] = "ok" if len(blocking) <= 2 else "fail"
        gates["acceptance_criteria"] = (
            "ok"
            if all(r.acceptance_criteria for r in doc.requirements if r.priority == "must")
            else "fail"
        )
        gates["has_must"] = "ok" if any(r.priority == "must" for r in doc.requirements) else "fail"

        artifacts = {"requirements.json": json.loads(doc.model_dump_json())}
        return AgentResult(
            artifacts=artifacts,
            gates=gates,
            questions_blocking=len(blocking),
        )
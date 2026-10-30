"""UI Design-агент: системная модель + API -> ui-spec.json.

Генерирует спецификацию интерфейса: потоки, экраны (состояния), действия.
Если LLM вернул пустой ответ — детерминированно строит экраны из
архитектурных операций, чтобы пайплайн оставался работоспособным.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.schemas.ui_spec import UiAction, UiScreen, UiSpec


class UiDesignAgent(BaseAgent[UiSpec]):
    """Агент проектирования интерфейса.

    Attributes:
        name: Имя этапа — ``04_ui_design``.
    """

    name = "04_ui_design"
    prompt_version = "v1"

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema артефакта UI."""
        return UiSpec.model_json_schema()

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: requirements + architecture + схема.

        Args:
            inputs: Входные данные с ключами ``requirements``,
                ``architecture`` (ArchitectureApi dict).

        Returns:
            Текст user-промпта.
        """
        requirements = inputs.get("requirements", {})
        arch = inputs.get("architecture", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — требования и архитектура. Спроектируй UI-спецификацию.\n\n"
            f"=== REQUIREMENTS.JSON ===\n{json.dumps(requirements, ensure_ascii=False, indent=2)}\n\n"
            f"=== ARCHITECTURE (operations) ===\n"
            f"{json.dumps(arch.get('operations', []), ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ: схема + gates (+ fallback экраны).

        Args:
            data: Ответ модели.
            inputs: Входные данные (architecture).

        Returns:
            AgentResult с артефактом ``ui-spec.json`` и gates.
        """
        spec = UiSpec.model_validate(data)

        # Детерминированный fallback: если экранов нет — построить из операций.
        architecture = inputs.get("architecture") or {}
        raw_ops = architecture.get("operations") or []
        if not spec.screens and raw_ops:
            spec = self._fallback_screens(spec, raw_ops)

        # Gates.
        gates: dict[str, str] = {}
        gates["schema"] = "ok"
        gates["screens_states"] = (
            "ok"
            if all(
                "empty" in s.states and "loading" in s.states and "error" in s.states
                for s in spec.screens
            )
            else "fail"
        )
        # Каждая action.api_operation_id существует в openapi.
        known_ids = {op.get("operationId") for op in raw_ops}
        gates["actions_valid"] = (
            "ok"
            if all(
                a.api_operation_id is None or a.api_operation_id in known_ids
                for s in spec.screens
                for a in s.actions
            )
            else "fail"
        )
        gates["screens_nonempty"] = "ok" if spec.screens else "fail"

        artifacts = {"ui-spec.json": json.loads(spec.model_dump_json())}
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

    @staticmethod
    def _fallback_screens(spec: UiSpec, raw_ops: list[dict[str, Any]]) -> UiSpec:
        """Построить экраны из операций API (fallback при пустом ответе).

        Args:
            spec: Существующая (возможно, пустая) спецификация.
            raw_ops: Операции из architecture (list of dict).

        Returns:
            UiSpec с экранами, построенными из операций.
        """
        screens = list(spec.screens)
        for i, op in enumerate(raw_ops, start=1):
            operation_id = op.get("operationId", f"op-{i}")
            screen = UiScreen(
                id=f"SCR-{i:03d}",
                title=op.get("summary") or operation_id,
                requirement_ids=op.get("requirement_ids", []),
                states={
                    "empty": "Нет данных",
                    "loading": "Загрузка...",
                    "error": "Ошибка загрузки",
                    "forbidden": "Доступ запрещён" if op.get("auth") else "",
                },
                actions=[
                    UiAction(
                        id=f"ACT-{i:03d}",
                        label="Открыть",
                        api_operation_id=operation_id,
                        navigates_to=None,
                    )
                ],
            )
            screens.append(screen)
        return UiSpec(flows=spec.flows, screens=screens, components=spec.components)

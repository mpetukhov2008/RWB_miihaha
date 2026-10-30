"""Mock-режим LLM: детерминированные ответы без сети.

Используется для демо-прогонов (``LLM_MODE=mock``) и для тестов пайплайна.
Ответы подбираются по имени этапа из реестра; реестр наполняется по мере
реализации агентов (фазы 2–6).
"""

from __future__ import annotations

from typing import Any

from pipeline.errors import LLMUnavailable

# Реестр предзаданных ответов по имени этапа.
# Заполняется в фазах 2–6 (requirements, system_analysis, ui, docs).
DEFAULT_MOCK_RESPONSES: dict[str, dict[str, Any]] = {}


class MockBackend:
    """Детерминированный источник ответов для режима ``LLM_MODE=mock``.

    Args:
        responses: Словарь «имя этапа -> JSON-ответ». Если не задан,
            используется общий реестр :data:`DEFAULT_MOCK_RESPONSES`.
    """

    def __init__(
        self,
        responses: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.responses = responses if responses is not None else DEFAULT_MOCK_RESPONSES

    def complete(
        self,
        stage: str,
        prompt_version: str,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Вернуть предзаданный ответ для этапа.

        Args:
            stage: Имя этапа.
            prompt_version: Версия промпта (не влияет на ответ).
            system_prompt: Системный промпт (игнорируется).
            user_prompt: Пользовательский промпт (игнорируется).
            json_schema: JSON Schema ответа (игнорируется).

        Returns:
            Предзаданный JSON-ответ.

        Raises:
            LLMUnavailable: Если для этапа нет предзаданного ответа.
        """
        try:
            return self.responses[stage]
        except KeyError:
            raise LLMUnavailable(
                f"MockLLM: нет предзаданного ответа для этапа {stage!r}; "
                "наполните реестр DEFAULT_MOCK_RESPONSES"
            ) from None
"""FakeLLM: заглушка LLM-клиента для тестов агентов и оркестратора.

Ответы задаются списком; каждый вызов ``complete_json`` возвращает следующий
по индексу. Если ответов не хватило — поднимается ошибка, чтобы тесты не
прошли «молча». FakeLLM повторяет публичный контракт ``LLMClient.complete_json``,
поэтому может подставляться вместо реального клиента (duck typing).
"""

from __future__ import annotations

from typing import Any


class FakeLLM:
    """Заглушка LLM-клиента с предзаданными ответами.

    Args:
        answers: Список JSON-объектов, возвращаемых по очереди.
    """

    def __init__(self, answers: list[dict[str, Any]]) -> None:
        self.answers = answers
        self.call_count = 0

    def complete_json(
        self,
        stage: str,
        prompt_version: str,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any] | None = None,
        attempt: int = 1,
    ) -> dict[str, Any]:
        """Вернуть следующий предзаданный ответ (метод-заглушка)."""
        if self.call_count >= len(self.answers):
            raise AssertionError(
                f"FakeLLM: запрошено больше ответов ({self.call_count + 1}), "
                f"чем задано ({len(self.answers)})"
            )
        answer = self.answers[self.call_count]
        self.call_count += 1
        return answer

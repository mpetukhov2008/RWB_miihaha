"""Базовый агент: единый контракт run / retry / валидация.

Схема важнее промпта: ответ модели валидируется Pydantic, а ошибка
валидации превращается в retry с текстом ошибки, а не в «добавить
правил в промпт».
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from pipeline.agents.prompts import load_prompt
from pipeline.errors import LLMUnavailable, ValidationFailed

TArtifact = TypeVar("TArtifact", bound=BaseModel)


class AgentResult:
    """Результат работы агента: артефакты, gates, число blocking-вопросов.

    Attributes:
        artifacts: Словарь «имя файла -> содержимое артефакта».
        gates: Словарь «имя gate -> статус (ok/fail)».
        questions_blocking: Количество blocking-вопросов в артефакте.
    """

    def __init__(
        self,
        artifacts: dict[str, Any],
        gates: dict[str, str],
        questions_blocking: int = 0,
    ) -> None:
        self.artifacts = artifacts
        self.gates = gates
        self.questions_blocking = questions_blocking

    def ok(self) -> bool:
        """Все gates прошли.

        Returns:
            ``True``, если нет ни одного gate со статусом ``fail``.
        """
        return "fail" not in self.gates.values()


class BaseAgent(ABC, Generic[TArtifact]):
    """Абстрактный агент пайплайна.

    Attributes:
        name: Имя этапа (ключ в state.json, кэше и логах).
        prompt_version: Версия промпта (``v1``, ``v2``, ...).
        stage_dir: Директория этапа внутри прогона.
    """

    name: str = ""
    prompt_version: str = "v1"

    def __init__(self, llm: Any, run_dir: Path) -> None:
        """Инициализировать агента.

        Args:
            llm: LLM-клиент (LLMClient или FakeLLM).
            run_dir: Корень прогона (``runs/{run_id}/``).
        """
        self.llm = llm
        self.run_dir = run_dir
        self.stage_dir = run_dir / self.name
        self.stage_dir.mkdir(parents=True, exist_ok=True)

    @property
    def system_prompt(self) -> str:
        """Системный промпт из ``prompts/{name}/{prompt_version}.md``."""
        return load_prompt(self.name, self.prompt_version)

    @abstractmethod
    def json_schema(self) -> dict[str, Any]:
        """JSON Schema ожидаемого ответа (Pydantic model_json_schema)."""

    @abstractmethod
    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт из входных данных этапа."""

    @abstractmethod
    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ модели: схема + gates + артефакты."""

    def run(self, inputs: dict[str, Any], max_retries: int = 2) -> AgentResult:
        """Выполнить этап: вызов LLM с retry по валидации.

        Args:
            inputs: Входные данные этапа (предыдущие артефакты и т.п.).
            max_retries: Максимальное число повторных вызовов после ошибки
                валидации (сверх первого).

        Returns:
            Результат агента (артефакты + gates).

        Raises:
            ValidationFailed: Если после всех попыток ответ не прошёл валидацию.
            LLMUnavailable: Если LLM недоступен.
        """
        schema = self.json_schema()
        user_prompt = self.build_user_prompt(inputs)

        last_error: str | None = None
        for attempt in range(1, max_retries + 2):
            prompt = user_prompt
            if last_error is not None:
                prompt = self._retry_hint(prompt, last_error)
            try:
                data = self.llm.complete_json(
                    stage=self.name,
                    prompt_version=self.prompt_version,
                    system_prompt=self.system_prompt,
                    user_prompt=prompt,
                    json_schema=schema,
                    attempt=attempt,
                )
                return self.validate(data, inputs)
            except ValidationError as exc:
                last_error = str(exc)
        raise ValidationFailed(
            f"Этап {self.name!r}: ответ модели не прошёл валидацию "
            f"за {max_retries + 1} попыток. Последняя ошибка: {last_error}"
        )

    @staticmethod
    def _retry_hint(user_prompt: str, err: str) -> str:
        """Добавить текст ошибки валидации в user-промпт.

        Args:
            user_prompt: Исходный user-промпт.
            err: Текст pydantic.ValidationError.

        Returns:
            Промпт с требованием вернуть только валидный JSON.
        """
        return (
            f"{user_prompt}\n\n"
            f"Предыдущий ответ не прошёл валидацию:\n{err}\n"
            f"Верни ТОЛЬКО валидный JSON."
        )

    @staticmethod
    def _dump(artifact: BaseModel | list[Any] | dict[str, Any]) -> dict[str, Any]:
        """Сериализовать артефакт в dict для записи на диск.

        Args:
            artifact: Pydantic-модель, список или словарь.

        Returns:
            JSON-совместимый словарь.
        """
        if isinstance(artifact, BaseModel):
            return json.loads(artifact.model_dump_json())
        if isinstance(artifact, list):
            return [json.loads(item.model_dump_json()) if isinstance(item, BaseModel) else item for item in artifact]
        return artifact
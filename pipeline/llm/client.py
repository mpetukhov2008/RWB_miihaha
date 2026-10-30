"""LLM-клиент для OpenAI-совместимых endpoint.

Отвечает за один сценарий: ``complete_json`` — вызов модели с гарантированным
JSON-ответом. Включает кэширование по хэшу запроса, запись метрик в JSONL
и retry на сетевые ошибки. Модель ничего не запускает — только возвращает JSON.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import APIConnectionError, APITimeoutError, OpenAI

from pipeline.config import LLM_NETWORK_RETRIES, LLM_TIMEOUT_SEC, Settings
from pipeline.errors import LLMUnavailable
from pipeline.llm.mock import MockBackend

logger = logging.getLogger(__name__)


@dataclass
class LLMMetrics:
    """Метрики одного вызова LLM (в том числе кэш-попадания)."""

    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    status: str = "ok"


class LLMClient:
    """Клиент с кэшем, метриками и retry.

    Args:
        run_dir: Директория прогона; внутри создаются ``cache/`` и ``logs/``.
        settings: Конфигурация из env (base_url, ключ, модель, режимы).
    """

    def __init__(self, run_dir: Path, settings: Settings | None = None) -> None:
        self.run_dir = run_dir
        self.cache_dir = run_dir / "cache"
        self.logs_dir = run_dir / "logs"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.settings = settings or Settings()
        self._mock_mode = self.settings.llm_mode == "mock"
        self._client = self._build_client()

    def _build_client(self) -> OpenAI | MockBackend:
        """Создать реальный клиент OpenAI или mock-бэкенд.

        В режиме ``LLM_MODE=mock`` сетевой клиент не создаётся — пайплайн
        работает без сети и без ключа (демо, CI).
        """
        if self._mock_mode:
            return MockBackend()
        return OpenAI(
            base_url=self.settings.llm_base_url,
            api_key=self.settings.llm_api_key or "not-set",
            timeout=LLM_TIMEOUT_SEC,
        )

    def _cache_key(
        self,
        stage: str,
        prompt_version: str,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """sha256-хэш запроса — ключ кэша.

        Args:
            stage: Имя этапа.
            prompt_version: Версия промпта (например, ``v1``).
            system_prompt: Системный промпт.
            user_prompt: Пользовательский промпт.

        Returns:
            Шестнадцатеричный хэш.
        """
        payload = "||".join([stage, prompt_version, system_prompt, user_prompt])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def _strip_markdown_fence(text: str) -> str:
        """Снять markdown-обёртку ```json ... ``` / ``` ... ``` с ответа.

        Args:
            text: Сырой ответ модели.

        Returns:
            Текст без обрамляющего фенса (если он был).
        """
        stripped = text.strip()
        if stripped.startswith("```"):
            lines = stripped.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            return "\n".join(lines).strip()
        return stripped

    def _read_cache(self, key: str) -> dict[str, Any] | None:
        """Прочитать ответ из кэша.

        Args:
            key: Ключ кэша.

        Returns:
            JSON-объект или ``None``, если кэш пуст/битый.
        """
        path = self.cache_dir / f"{key}.json"
        if not path.exists():
            return None
        try:
            loaded: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
            return loaded
        except (json.JSONDecodeError, OSError):
            logger.warning("Битый кэш: %s", path)
            return None

    def _write_cache(self, key: str, data: dict[str, Any]) -> None:
        """Записать ответ в кэш.

        Args:
            key: Ключ кэша.
            data: JSON-объект ответа.
        """
        path = self.cache_dir / f"{key}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _log_call(
        self,
        stage: str,
        attempt: int,
        metrics: LLMMetrics,
        model: str,
    ) -> None:
        """Дописать строку метрик вызова в ``logs/agent-calls.jsonl``.

        Args:
            stage: Имя этапа.
            attempt: Номер попытки.
            metrics: Метрики вызова.
            model: Имя модели.
        """
        record = {
            "ts": time.time(),
            "stage": stage,
            "attempt": attempt,
            "model": model,
            "tokens_in": metrics.tokens_in,
            "tokens_out": metrics.tokens_out,
            "latency_ms": metrics.latency_ms,
            "status": metrics.status,
        }
        with (self.logs_dir / "agent-calls.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def complete_json(
        self,
        stage: str,
        prompt_version: str,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any] | None = None,
        attempt: int = 1,
    ) -> dict[str, Any]:
        """Вызвать модель и вернуть JSON-объект.

        Args:
            stage: Имя этапа (для кэша и логов).
            prompt_version: Версия промпта.
            system_prompt: Системный промпт.
            user_prompt: Пользовательский промпт.
            json_schema: JSON Schema ожидаемого ответа (передаётся модели).
            attempt: Номер попытки (для retry на уровне агента).

        Returns:
            JSON-объект ответа модели.

        Raises:
            LLMUnavailable: При исчерпании сетевых retry.
        """
        key = self._cache_key(stage, prompt_version, system_prompt, user_prompt)
        cached = self._read_cache(key)
        if cached is not None:
            self._log_call(stage, attempt, LLMMetrics(status="cache_hit"), self.settings.llm_model)
            return cached

        if self._mock_mode:
            started = time.monotonic()
            data = self._mock_call(stage, system_prompt, user_prompt, json_schema)
            latency_ms = int((time.monotonic() - started) * 1000)
            self._log_call(
                stage,
                attempt,
                LLMMetrics(tokens_in=0, tokens_out=0, latency_ms=latency_ms, status="ok"),
                self.settings.llm_model,
            )
            self._write_cache(key, data)
            return data

        last_error: Exception | None = None
        for network_attempt in range(1, LLM_NETWORK_RETRIES + 1):
            try:
                started = time.monotonic()
                data = self._call(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )
                latency_ms = int((time.monotonic() - started) * 1000)
                self._log_call(
                    stage,
                    attempt,
                    LLMMetrics(
                        tokens_in=data.tokens_in,
                        tokens_out=data.tokens_out,
                        latency_ms=latency_ms,
                        status="ok",
                    ),
                    data.model,
                )
                self._write_cache(key, data.content)
                return data.content
            except (APITimeoutError, APIConnectionError) as exc:  # noqa: PERF203
                last_error = exc
                logger.warning(
                    "Сетевая ошибка LLM (попытка %s/%s): %s",
                    network_attempt,
                    LLM_NETWORK_RETRIES,
                    exc,
                )
                time.sleep(1.0 * network_attempt)
        raise LLMUnavailable(f"LLM недоступен после {LLM_NETWORK_RETRIES} попыток: {last_error}")

    def _mock_call(
        self,
        stage: str,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Вызвать mock-бэкенд (без сети).

        Args:
            stage: Имя этапа.
            system_prompt: Системный промпт.
            user_prompt: Пользовательский промпт.
            json_schema: JSON Schema ответа.

        Returns:
            Предзаданный JSON-ответ.
        """
        client = self._client
        assert isinstance(client, MockBackend)
        result: dict[str, Any] = client.complete(
            stage, self.settings.llm_model, system_prompt, user_prompt, json_schema
        )
        return result

    def _call(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> Any:
        """Один сетевой вызов chat.completions.create (без retry).

        Args:
            system_prompt: Системный промпт.
            user_prompt: Пользовательский промпт.

        Returns:
            Объект ответа OpenAI с полями ``content``, ``tokens_in``,
            ``tokens_out`` и ``model``.
        """
        kwargs: dict[str, Any] = {
            "model": self.settings.llm_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.0,
        }
        if self.settings.llm_json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        # JSON Schema не отправляется отдельным параметром (не все
        # Qwen-эндпоинты его поддерживают); схема передаётся модели
        # внутри user-промпта агентом в build_user_prompt.

        openai_client = self._client
        assert not isinstance(openai_client, MockBackend)
        response = openai_client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content or ""
        usage = response.usage
        return _OpenAIResponse(
            content=self._parse_json(content),
            tokens_in=usage.prompt_tokens if usage else 0,
            tokens_out=usage.completion_tokens if usage else 0,
            model=response.model,
        )

    def _parse_json(self, content: str) -> dict[str, Any]:
        """Распарсить JSON из ответа, сняв markdown-обёртку.

        Args:
            content: Сырой текст ответа модели.

        Returns:
            JSON-объект.

        Raises:
            LLMUnavailable: Если ответ не является валидным JSON-объектом.
        """
        text = self._strip_markdown_fence(content)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMUnavailable(f"Ответ модели не является JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise LLMUnavailable("Ответ модели — не JSON-объект")
        return data


class _OpenAIResponse:
    """Лёгкая обёртка над ответом OpenAI для тестов и типизации."""

    def __init__(
        self,
        content: dict[str, Any],
        tokens_in: int,
        tokens_out: int,
        model: str,
    ) -> None:
        self.content = content
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.model = model

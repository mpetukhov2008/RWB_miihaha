"""Тесты LLMClient: кэш, метрики, markdown-fence, сетевые retry."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from openai import APIConnectionError, APITimeoutError

from pipeline.config import Settings
from pipeline.errors import LLMUnavailable
from pipeline.llm.client import LLMClient


def _response(content: str) -> SimpleNamespace:
    """Собрать поддельный ответ OpenAI."""
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5),
        model="fake-model",
    )


class _FakeCompletions:
    """Поддельный chat.completions с заданным поведением."""

    def __init__(self, parent: "_FakeOpenAI") -> None:
        self._parent = parent

    def create(self, **kwargs: object) -> object:
        self._parent.calls.append(kwargs)
        if self._parent.error is not None:
            raise self._parent.error
        return _response(self._parent.response_text)


class _FakeOpenAI:
    """Поддельный клиент openai.OpenAI (свойства вместо методов)."""

    def __init__(self, response_text: str = "", error: Exception | None = None) -> None:
        self.response_text = response_text
        self.error = error
        self.calls: list[dict] = []

    @property
    def chat(self) -> SimpleNamespace:
        return SimpleNamespace(completions=_FakeCompletions(self))


def _make_client(tmp_path: Path, fake: object, monkeypatch: pytest.MonkeyPatch) -> LLMClient:
    """LLMClient с подменённым сетевым клиентом."""
    monkeypatch.delenv("LLM_MODE", raising=False)
    client = LLMClient(tmp_path, settings=Settings())
    client._client = fake  # type: ignore[assignment]
    return client


def test_cache_second_call_no_network(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Второй вызов с тем же запросом не ходит в сеть (cache_hit)."""
    fake = _FakeOpenAI(response_text='{"ok": true}')
    client = _make_client(tmp_path, fake, monkeypatch)

    r1 = client.complete_json("req", "v1", "sys", "user", {"type": "object"})
    r2 = client.complete_json("req", "v1", "sys", "user", {"type": "object"})

    assert r1 == {"ok": True}
    assert r2 == {"ok": True}
    assert len(fake.calls) == 1  # сетевой вызов был только один

    # Метрики: первый — ok, второй — cache_hit.
    log = (tmp_path / "logs" / "agent-calls.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(log) == 2
    first = json.loads(log[0])
    second = json.loads(log[1])
    assert first["status"] == "ok" and first["tokens_in"] == 10 and first["tokens_out"] == 5
    assert second["status"] == "cache_hit"
    assert second["tokens_in"] == 0 and second["tokens_out"] == 0


def test_strip_markdown_fence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ответ в ```json ... ``` корректно распарсивается."""
    fake = _FakeOpenAI(response_text='```json\n{"a": 1}\n```')
    client = _make_client(tmp_path, fake, monkeypatch)

    data = client.complete_json("stage", "v1", "sys", "user")
    assert data == {"a": 1}


def test_network_retry_then_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Таймаут -> retry -> успех; метрики пишутся."""
    calls = {"n": 0}

    class FlakyCompletions:
        def __init__(self, parent: "Flaky") -> None:
            self._parent = parent

        def create(self, **kwargs: object) -> object:
            self._parent.calls.append(kwargs)
            calls["n"] += 1
            if calls["n"] == 1:
                raise APITimeoutError("timeout")
            return _response('{"ok": 1}')

    class Flaky:
        def __init__(self) -> None:
            self.calls: list[dict] = []

        @property
        def chat(self) -> SimpleNamespace:
            return SimpleNamespace(completions=FlakyCompletions(self))

    flaky = Flaky()
    client = _make_client(tmp_path, flaky, monkeypatch)

    data = client.complete_json("stage", "v1", "sys", "user")
    assert data == {"ok": 1}
    assert len(flaky.calls) == 2


def test_network_error_exhausted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Все сетевые попытки провалились -> LLMUnavailable."""
    fake = _FakeOpenAI(error=APIConnectionError(request=None))
    client = _make_client(tmp_path, fake, monkeypatch)

    with pytest.raises(LLMUnavailable):
        client.complete_json("stage", "v1", "sys", "user")
    assert len(fake.calls) == 2  # LLM_NETWORK_RETRIES


def test_invalid_json_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Не-JSON ответ -> LLMUnavailable."""
    fake = _FakeOpenAI(response_text="не json")
    client = _make_client(tmp_path, fake, monkeypatch)

    with pytest.raises(LLMUnavailable):
        client.complete_json("stage", "v1", "sys", "user")


def test_json_mode_off_no_response_format(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """При LLM_JSON_MODE=0 параметр response_format не передаётся."""
    monkeypatch.setenv("LLM_JSON_MODE", "0")
    fake = _FakeOpenAI(response_text='{"ok": 1}')
    client = _make_client(tmp_path, fake, monkeypatch)

    client.complete_json("stage", "v1", "sys", "user")
    assert "response_format" not in fake.calls[0]
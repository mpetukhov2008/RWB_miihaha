"""Тесты оркестратора: happy path, Question Gate, пропуск done-этапов."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from pipeline.agents.base import AgentResult
from pipeline.config import Settings
from pipeline.errors import StageFailed
from pipeline.pipeline import orchestrator
from pipeline.pipeline.state import RunState


class FakeAgentA:
    """Фейковый агент первого этапа (счётчик вызовов в классе)."""

    name = "alpha"
    prompt_version = "v1"
    calls = 0

    def __init__(self, llm: Any, run_dir: Path) -> None:
        self.llm = llm
        self.run_dir = run_dir

    def run(self, inputs: dict[str, Any]) -> AgentResult:
        FakeAgentA.calls += 1
        return AgentResult(
            artifacts={"alpha.json": {"ok": True}},
            gates={"g1": "ok"},
            questions_blocking=0,
        )


class FakeAgentB:
    """Фейковый агент второго этапа."""

    name = "beta"
    prompt_version = "v1"
    calls = 0

    def __init__(self, llm: Any, run_dir: Path) -> None:
        self.llm = llm
        self.run_dir = run_dir

    def run(self, inputs: dict[str, Any]) -> AgentResult:
        FakeAgentB.calls += 1
        return AgentResult(
            artifacts={"beta.json": {"ok": True}},
            gates={"g2": "ok"},
            questions_blocking=0,
        )


class BlockingAgent:
    """Фейковый агент, возвращающий blocking-вопрос."""

    name = "gamma"
    prompt_version = "v1"

    def __init__(self, llm: Any, run_dir: Path) -> None:
        self.llm = llm
        self.run_dir = run_dir

    def run(self, inputs: dict[str, Any]) -> AgentResult:
        return AgentResult(
            artifacts={"gamma.json": {"ok": True}},
            gates={"g3": "ok"},
            questions_blocking=2,
        )


@pytest.fixture(autouse=True)
def _reset_counters() -> None:
    """Сбросить счётчики вызовов фейковых агентов между тестами."""
    FakeAgentA.calls = 0
    FakeAgentB.calls = 0


def _mock_settings() -> Settings:
    """Settings в mock-режиме — LLMClient не ходит в сеть."""
    return Settings()


def test_happy_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Два агента проходят: артефакты записаны, state — done."""
    monkeypatch.setattr(orchestrator, "STAGES", [("alpha", FakeAgentA), ("beta", FakeAgentB)])
    run_dir = tmp_path / "run-1"

    result = orchestrator.run_pipeline(
        run_dir=run_dir,
        requirements_md="текст",
        answers=None,
        settings=_mock_settings(),
    )

    assert result == "done"
    assert FakeAgentA.calls == 1 and FakeAgentB.calls == 1
    assert (run_dir / "alpha" / "alpha.json").exists()
    assert (run_dir / "beta" / "beta.json").exists()

    state = RunState(run_dir)
    assert state.stage_status("alpha") == "done"
    assert state.stage_status("beta") == "done"
    assert state.data["stages"]["alpha"]["gates"] == {"g1": "ok"}


def test_stops_on_blocking_question(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Blocking-вопрос -> waiting_answers, артефакты НЕ персистятся."""
    monkeypatch.setattr(orchestrator, "STAGES", [("gamma", BlockingAgent)])
    run_dir = tmp_path / "run-2"

    result = orchestrator.run_pipeline(
        run_dir=run_dir,
        requirements_md="текст",
        answers=None,
        settings=_mock_settings(),
    )

    assert result == "waiting_answers"
    state = RunState(run_dir)
    assert state.stage_status("gamma") == "waiting_answers"
    # Артефакты не записаны, пока нет ответов.
    assert not (run_dir / "gamma" / "gamma.json").exists()


def test_skips_done_stages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Этап со статусом done пропускается (агент не вызывается)."""
    monkeypatch.setattr(orchestrator, "STAGES", [("alpha", FakeAgentA), ("beta", FakeAgentB)])
    run_dir = tmp_path / "run-3"

    # Первый этап уже завершён в state.json.
    state = RunState(run_dir)
    state.start_stage("alpha", "v1")
    state.finish_stage("alpha", {"g1": "ok"})

    result = orchestrator.run_pipeline(
        run_dir=run_dir,
        requirements_md="текст",
        answers=None,
        settings=_mock_settings(),
    )

    assert result == "done"
    assert FakeAgentA.calls == 0  # пропущен
    assert FakeAgentB.calls == 1  # выполнен


def test_stage_failure_marks_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Исключение в агенте -> StageFailed и статус failed."""

    class ExplodingAgent:
        name = "explode"
        prompt_version = "v1"

        def __init__(self, llm: Any, run_dir: Path) -> None:
            self.llm = llm
            self.run_dir = run_dir

        def run(self, inputs: dict[str, Any]) -> AgentResult:
            raise RuntimeError("boom")

    monkeypatch.setattr(orchestrator, "STAGES", [("explode", ExplodingAgent)])
    run_dir = tmp_path / "run-4"

    with pytest.raises(StageFailed):
        orchestrator.run_pipeline(
            run_dir=run_dir,
            requirements_md="текст",
            answers=None,
            settings=_mock_settings(),
        )

    state = RunState(run_dir)
    assert state.stage_status("explode") == "failed"
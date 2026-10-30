"""Тесты System Analysis-агента: happy path и negative (пустые сценарии)."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.system_analysis import SystemAnalysisAgent
from tests.fake_llm import FakeLLM

VALID = {
    "boundaries": {"inside": ["Сессии"], "outside": ["Гео"]},
    "roles_permissions": [{"role": "Водитель", "permissions": ["Начать сессию"]}],
    "scenarios": [
        {
            "id": "US-001",
            "title": "Начало сессии",
            "actor": "Водитель",
            "requirement_ids": ["FR-001"],
            "steps": ["Открыть", "Начать"],
            "result": "Сессия создана",
        }
    ],
    "entities": [{"name": "Session", "description": "Сессия"}],
    "assumptions": ["Одна сессия"],
    "open_questions": [],
}

EMPTY_SCENARIOS = {**VALID, "scenarios": []}


def _inputs() -> dict:
    return {"requirements": {"requirements": [{"id": "FR-001", "priority": "must"}]}}


def test_happy_path(tmp_path: Path) -> None:
    """Валидный ответ -> system-analysis.md сгенерирован, gates ok."""
    agent = SystemAnalysisAgent(FakeLLM([VALID]), tmp_path)
    result = agent.run(_inputs())

    assert result.ok() is True
    assert "system-analysis.md" in result.artifacts
    md = result.artifacts["system-analysis.md"]
    assert "US-001" in md
    assert "Начало сессии" in md


def test_empty_scenarios_gate_fail(tmp_path: Path) -> None:
    """Пустые сценарии -> gate scenarios_nonempty=fail."""
    agent = SystemAnalysisAgent(FakeLLM([EMPTY_SCENARIOS]), tmp_path)
    result = agent.run(_inputs())

    assert result.gates["scenarios_nonempty"] == "fail"
    assert result.ok() is False
"""Тесты Tests-агента: happy path и must-покрытие."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.tests_agent import TestsAgent
from tests.fake_llm import FakeLLM

VALID = {
    "api_tests": [
        {
            "name": "Старт сессии",
            "method": "post",
            "path": "/sessions",
            "cases": [
                {"title": "OK", "expected_status": 201, "payload": {"zoneId": "z1"}},
                {"title": "Bad", "expected_status": 400, "payload": None},
            ],
        }
    ],
    "e2e_tests": [
        {"name": "Старт", "scenario_id": "FR-001", "steps": ["Открыть", "Начать"]}
    ],
}

NO_COVERAGE = {"api_tests": VALID["api_tests"], "e2e_tests": []}


def _inputs() -> dict:
    return {"requirements": {"requirements": [{"id": "FR-001", "priority": "must"}]}}


def test_happy_path(tmp_path: Path) -> None:
    """Валидный ответ -> артефакты тестов + отчёт, gates ok."""
    agent = TestsAgent(FakeLLM([VALID]), tmp_path)
    result = agent.run(_inputs())

    assert result.ok() is True
    assert "tests/api-tests.json" in result.artifacts
    assert "tests/e2e-tests.json" in result.artifacts
    report = result.artifacts["tests/test-report.md"]
    assert "FR-001" in report
    assert "Не покрыто: —" in report


def test_must_not_covered_gate_fail(tmp_path: Path) -> None:
    """Нет e2e на must-FR -> gate must_coverage=fail."""
    agent = TestsAgent(FakeLLM([NO_COVERAGE]), tmp_path)
    result = agent.run(_inputs())

    assert result.gates["must_coverage"] == "fail"
    assert result.ok() is False
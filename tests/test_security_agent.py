"""Тесты Security Report-агента."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.security_agent import SecurityReportAgent
from tests.fake_llm import FakeLLM

VALID = {
    "summary": "Всё в порядке",
    "findings": [
        {
            "severity": "low",
            "title": "Rate limit",
            "description": "Единый лимит",
            "status": "open",
        }
    ],
}

EMPTY = {"summary": "Нет находок", "findings": []}


def test_happy_path(tmp_path: Path) -> None:
    """Валидный ответ -> security-report.md с таблицей findings."""
    agent = SecurityReportAgent(FakeLLM([VALID]), tmp_path)
    result = agent.run({"architecture": {}})

    assert result.ok() is True
    report = result.artifacts["reports/security-report.md"]
    assert "Rate limit" in report
    assert "open" in report


def test_empty_findings_gate_fail(tmp_path: Path) -> None:
    """Пустые findings -> gate findings_nonempty=fail."""
    agent = SecurityReportAgent(FakeLLM([EMPTY]), tmp_path)
    result = agent.run({"architecture": {}})

    assert result.gates["findings_nonempty"] == "fail"
    assert result.ok() is False
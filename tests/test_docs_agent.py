"""Тесты Docs-агента: gates на README/must-FR/assumptions."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.docs_agent import DocsAgent
from tests.fake_llm import FakeLLM

VALID = {
    "files": [
        {"path": "README.md", "content": "## install\n## run\n## test"},
        {"path": "docs/user-guide.md", "content": "FR-001 описан"},
        {"path": "docs/known-limitations.md", "content": "Допущение про геолокацию"},
    ]
}

BAD = {
    "files": [
        {"path": "README.md", "content": "нет команд"},
        {"path": "docs/user-guide.md", "content": "пусто"},
        {"path": "docs/known-limitations.md", "content": "пусто"},
    ]
}


def _inputs() -> dict:
    return {
        "requirements": {
            "requirements": [{"id": "FR-001", "priority": "must"}],
            "assumptions": ["Допущение про геолокацию"],
        }
    }


def test_happy_path(tmp_path: Path) -> None:
    """Все gates ok, артефакты с префиксом docs/."""
    agent = DocsAgent(FakeLLM([VALID]), tmp_path)
    result = agent.run(_inputs())

    assert result.ok() is True
    assert "docs/README.md" in result.artifacts
    assert result.gates["readme_commands"] == "ok"
    assert result.gates["user_guide_must"] == "ok"
    assert result.gates["limitations_assumptions"] == "ok"


def test_bad_docs_gates_fail(tmp_path: Path) -> None:
    """README без команд и без must-FR -> gates fail."""
    agent = DocsAgent(FakeLLM([BAD]), tmp_path)
    result = agent.run(_inputs())

    assert result.gates["readme_commands"] == "fail"
    assert result.gates["user_guide_must"] == "fail"
    assert result.gates["limitations_assumptions"] == "fail"
    assert result.ok() is False

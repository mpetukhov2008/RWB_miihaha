"""Тест Question Gate: blocking-вопросы, ответы и default_if_unanswered."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.requirements import RequirementsAgent
from tests.fake_llm import FakeLLM
from tests.fixtures import REQ


def test_blocking_with_answer_does_not_stop(tmp_path: Path) -> None:
    """Если на blocking-вопрос есть ответ — прогон не останавливается."""
    agent = RequirementsAgent(FakeLLM([dict(REQ)]), tmp_path)
    result = agent.run({"requirements_md": "x", "answers": {"Q-001": "20.1.6"}})
    assert result.questions_blocking == 0


def test_blocking_with_default_does_not_stop(tmp_path: Path) -> None:
    """Blocking-вопрос с default_if_unanswered разблокируется сам."""
    agent = RequirementsAgent(FakeLLM([dict(REQ)]), tmp_path)
    result = agent.run({"requirements_md": "x", "answers": {}})
    # Q-001 имеет default_if_unanswered="20.1.6" -> не блокирует.
    assert result.questions_blocking == 0


def test_blocking_without_answer_or_default_stops(tmp_path: Path) -> None:
    """Blocking-вопрос без ответа и без default — прогон останавливается."""
    data = {
        **REQ,
        "open_questions": [
            {
                "id": "Q-002",
                "text": "Без default",
                "severity": "blocking",
                "impact": "architecture",
                "options": [],
                "default_if_unanswered": None,
            }
        ],
    }
    agent = RequirementsAgent(FakeLLM([data]), tmp_path)
    result = agent.run({"requirements_md": "x", "answers": {}})
    assert result.questions_blocking == 1
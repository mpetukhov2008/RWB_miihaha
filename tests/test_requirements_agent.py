"""Тесты Requirements-агента: happy path и retry после невалидного ID."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.agents.requirements import RequirementsAgent
from pipeline.errors import ValidationFailed
from tests.fake_llm import FakeLLM

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _inputs() -> dict:
    return {"requirements_md": "Бизнес-требования", "answers": {}}


def test_happy_path(tmp_path: Path) -> None:
    """Валидный ответ -> AgentResult с ok-gates и артефактом requirements.json."""
    fake = FakeLLM([_load("requirements_good.json")])
    agent = RequirementsAgent(fake, tmp_path)

    result = agent.run(_inputs())

    assert result.ok() is True
    # Q-001 — blocking, но с default_if_unanswered, поэтому не останавливает
    # прогон (см. tests/test_question_gate.py).
    assert result.questions_blocking == 0
    assert set(result.gates) == {
        "schema",
        "unique_ids",
        "questions_limit",
        "blocking_limit",
        "acceptance_criteria",
        "has_must",
    }
    assert result.gates["unique_ids"] == "ok"
    assert result.gates["acceptance_criteria"] == "ok"
    artifact = result.artifacts["requirements.json"]
    assert artifact["requirements"][0]["id"] == "FR-001"
    # Артефакты пишет на диск оркестратор (фаза 3); агент их возвращает.


def test_retry_after_invalid_id(tmp_path: Path) -> None:
    """Первый ответ с невалидным ID -> retry с хинтом -> успех."""
    bad = _load("requirements_bad_ids.json")  # FR-1 / R-1 / дубликат FR-001
    good = _load("requirements_good.json")
    fake = FakeLLM([bad, good])
    agent = RequirementsAgent(fake, tmp_path)

    result = agent.run(_inputs())

    assert fake.call_count == 2
    assert result.ok() is True
    # Хинт с текстом ошибки валидации был добавлен во второй user-промпт
    # (проверяем косвенно: FakeLLM не хранит промпты, но второй ответ принят).


def test_retry_exhausted_raises(tmp_path: Path) -> None:
    """Все попытки невалидны -> ValidationFailed."""
    bad = _load("requirements_bad_ids.json")
    fake = FakeLLM([bad, bad, bad])
    agent = RequirementsAgent(fake, tmp_path)

    with pytest.raises(ValidationFailed):
        agent.run(_inputs(), max_retries=2)


def test_questions_limit_gate_fail(tmp_path: Path) -> None:
    """Больше 5 вопросов -> gate questions_limit=fail (но схема валидна)."""
    data = _load("requirements_good.json")
    data["open_questions"] = [
        {
            "id": f"Q-{i:03d}",
            "text": f"Вопрос {i}",
            "severity": "minor",
            "impact": "other",
            "options": [],
            "default_if_unanswered": None,
        }
        for i in range(1, 7)
    ]
    fake = FakeLLM([data])
    agent = RequirementsAgent(fake, tmp_path)

    result = agent.run(_inputs())

    assert result.gates["questions_limit"] == "fail"
    assert result.ok() is False

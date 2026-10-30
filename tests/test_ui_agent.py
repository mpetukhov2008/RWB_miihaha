"""Тесты UI Design-агента: happy path и fallback-экраны."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.ui import UiDesignAgent
from tests.fake_llm import FakeLLM

VALID = {
    "flows": [{"id": "FLOW-001", "name": "Старт", "steps": ["SCR-001"]}],
    "screens": [
        {
            "id": "SCR-001",
            "title": "Зона",
            "requirement_ids": ["FR-001"],
            "states": {"empty": "нет", "loading": "груз", "error": "ошибка", "forbidden": "", "success": "ок"},
            "actions": [{"id": "ACT-001", "label": "Начать", "api_operation_id": "startSession", "navigates_to": None}],
        }
    ],
    "components": [{"name": "ZoneCard", "description": "Карточка"}],
}

EMPTY_SCREENS = {"flows": [], "screens": [], "components": []}


def _inputs() -> dict:
    return {
        "requirements": {"requirements": [{"id": "FR-001", "priority": "must"}]},
        "architecture": {
            "operations": [
                {
                    "method": "post",
                    "path": "/sessions",
                    "operationId": "startSession",
                    "summary": "Начать",
                    "requirement_ids": ["FR-001"],
                    "auth": True,
                }
            ]
        },
    }


def test_happy_path(tmp_path: Path) -> None:
    """Валидный ответ -> ui-spec.json, gates ok."""
    agent = UiDesignAgent(FakeLLM([VALID]), tmp_path)
    result = agent.run(_inputs())

    assert result.ok() is True
    spec = result.artifacts["ui-spec.json"]
    assert spec["screens"][0]["id"] == "SCR-001"
    assert "empty" in spec["screens"][0]["states"]


def test_fallback_screens_from_operations(tmp_path: Path) -> None:
    """Пустой ответ LLM -> экраны построены детерминированно из операций."""
    agent = UiDesignAgent(FakeLLM([EMPTY_SCREENS]), tmp_path)
    result = agent.run(_inputs())

    spec = result.artifacts["ui-spec.json"]
    assert len(spec["screens"]) == 1
    assert spec["screens"][0]["actions"][0]["api_operation_id"] == "startSession"
    assert result.ok() is True
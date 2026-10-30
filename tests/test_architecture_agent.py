"""Тесты Architecture API-агента: happy path и must-покрытие."""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.agents.architecture_api import ArchitectureApiAgent
from tests.fake_llm import FakeLLM

VALID = {
    "entities": [
        {
            "name": "Session",
            "description": "Сессия",
            "fields": [{"name": "id", "type": "string", "required": True}],
            "indexes": [],
        }
    ],
    "events": [
        {
            "name": "SessionStarted",
            "version": "1",
            "payload": {"sessionId": "string"},
            "idempotency_key": "sessionId",
            "description": "Старт",
        }
    ],
    "operations": [
        {
            "method": "post",
            "path": "/sessions",
            "operationId": "startSession",
            "summary": "Начать",
            "request_schema": {"type": "object"},
            "response_schema": {"type": "object"},
            "errors": ["400", "409"],
            "auth": True,
            "tags": ["sessions"],
            "requirement_ids": ["FR-001"],
            "error_schema": "ProblemDetails",
        }
    ],
}

MISSING_COVERAGE = {
    **VALID,
    "operations": [
        {
            **VALID["operations"][0],
            "requirement_ids": ["FR-002"],  # не покрывает must FR-001
        }
    ],
}


def _inputs() -> dict:
    return {"requirements": {"requirements": [{"id": "FR-001", "priority": "must"}]}}


def test_happy_path(tmp_path: Path) -> None:
    """Валидный ответ -> openapi.yaml, data-model.json, gates ok."""
    agent = ArchitectureApiAgent(FakeLLM([VALID]), tmp_path)
    result = agent.run(_inputs())

    assert result.ok() is True
    assert "openapi.yaml" in result.artifacts
    doc = yaml.safe_load(result.artifacts["openapi.yaml"])
    assert doc["openapi"] == "3.1.0"
    assert doc["paths"]["/sessions"]["post"]["x-requirement-ids"] == ["FR-001"]
    assert "ProblemDetails" in doc["components"]["schemas"]
    assert result.artifacts["architecture.json"]["entities"][0]["name"] == "Session"


def test_missing_must_coverage_gate_fail(tmp_path: Path) -> None:
    """must-FR не покрыт -> gate must_coverage=fail."""
    agent = ArchitectureApiAgent(FakeLLM([MISSING_COVERAGE]), tmp_path)
    result = agent.run(_inputs())

    assert result.gates["must_coverage"] == "fail"
    assert result.ok() is False

"""Общие JSON-фикстуры для тестов (импортируемые как модули)."""

from __future__ import annotations

REQ: dict = {
    "goals": ["Цель"],
    "roles": [{"id": "R-01", "name": "Водитель", "description": ""}],
    "requirements": [
        {
            "id": "FR-001",
            "type": "FR",
            "title": "Определение зоны",
            "description": "Определяет платную зону",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": ["Критерий"],
            "depends_on": [],
        }
    ],
    "constraints": [],
    "risks": [],
    "assumptions": ["Допущение"],
    "open_questions": [
        {
            "id": "Q-001",
            "text": "Какая версия Angular?",
            "severity": "blocking",
            "impact": "architecture",
            "options": ["17", "20.1.6"],
            "default_if_unanswered": "20.1.6",
        }
    ],
}

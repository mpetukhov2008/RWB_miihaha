"""Тесты детерминированных генераторов backend/frontend."""

from __future__ import annotations

from pipeline.generators.backend import build_backend_skeleton
from pipeline.generators.frontend import build_frontend_skeleton

OPENAPI = {"openapi": "3.1.0", "paths": {"/sessions": {"post": {}}}}
OPERATIONS = [
    {
        "method": "post",
        "path": "/sessions",
        "operationId": "startSession",
        "summary": "Начать",
        "tags": ["sessions"],
        "auth": True,
        "requirement_ids": ["FR-001"],
    }
]
ENTITIES = [
    {
        "name": "Session",
        "fields": [{"name": "id", "type": "string", "required": True}],
    }
]


def test_backend_skeleton_controllers_dtos_entities() -> None:
    """Генератор backend создаёт контроллеры по tags, DTO и сущности."""
    files = build_backend_skeleton(OPENAPI, OPERATIONS, ENTITIES)

    assert "Controllers/SessionsController.cs" in files
    assert "[HttpPost]" in files["Controllers/SessionsController.cs"]
    assert "[Authorize]" in files["Controllers/SessionsController.cs"]
    assert "Entities/Session.cs" in files


def test_frontend_skeleton_screens_routes_api() -> None:
    """Генератор frontend создаёт экраны, маршруты и API-сервис."""
    ui = {
        "screens": [
            {
                "id": "SCR-001",
                "title": "Зона",
                "states": {"empty": "нет", "loading": "груз", "error": "ошибка"},
                "actions": [{"label": "Начать", "api_operation_id": "startSession"}],
            }
        ]
    }
    files = build_frontend_skeleton(ui, OPERATIONS)

    assert "screens/SCR-001/Scr001.component.ts" in files
    assert "app/app.routes.ts" in files
    assert "app/services/api.service.ts" in files
    assert "startSession" in files["app/services/api.service.ts"]
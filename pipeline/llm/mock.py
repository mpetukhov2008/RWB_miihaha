"""Mock-режим LLM: детерминированные ответы без сети.

Используется для демо-прогонов (``LLM_MODE=mock``) и для CI. Ответы
подбираются по имени этапа из реестра. Реестр наполняется по мере
реализации агентов (фазы 2–6).
"""

from __future__ import annotations

from typing import Any

from pipeline.errors import LLMUnavailable

# Ответ Requirements-агента для демо-кейса «Парковочный помощник».
REQUIREMENTS_MOCK: dict[str, Any] = {
    "goals": [
        "Дать водителю возможность быстро начать и завершить парковочную сессию",
        "Автоматически фиксировать тариф и длительность сессии",
        "Информировать водителя о начале, окончании и превышении времени",
        "Дать админу панель для управления зонами, тарифами и сессиями",
    ],
    "roles": [
        {"id": "R-01", "name": "Водитель", "description": "Оплачивает парковку, управляет сессией, смотрит историю"},
        {"id": "R-02", "name": "Администратор", "description": "Управляет зонами, тарифами, просматривает сессии"},
    ],
    "requirements": [
        {
            "id": "FR-001",
            "type": "FR",
            "title": "Определение платной зоны",
            "description": "Приложение определяет платную зону по геолокации и показывает тариф",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "Если водитель вне платной зоны — сообщение «Вне платной зоны»",
                "Если внутри — название зоны, тариф и кнопка «Начать сессию»",
            ],
            "depends_on": [],
        },
        {
            "id": "FR-002",
            "type": "FR",
            "title": "Активная парковочная сессия",
            "description": "Водитель начинает и завершает сессию; система фиксирует время и тариф",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "После старта виден таймер и текущая стоимость",
                "Повторный старт в той же зоне невозможен при активной сессии",
                "Завершение фиксирует время окончания и итоговую стоимость",
            ],
            "depends_on": ["FR-001"],
        },
        {
            "id": "FR-003",
            "type": "FR",
            "title": "Уведомления",
            "description": "Уведомления о старте, за 5 минут до окончания и о превышении времени",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "Уведомление о старте сразу после начала сессии",
                "Уведомление за 5 минут до окончания",
                "Уведомление о превышении сразу после истечения",
            ],
            "depends_on": ["FR-002"],
        },
        {
            "id": "FR-004",
            "type": "FR",
            "title": "История парковок",
            "description": "Водитель смотрит историю сессий: дата, зона, длительность, стоимость, статус",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "История отсортирована по дате начала (новые сверху)",
                "Каждая запись содержит зону, длительность, стоимость и статус",
            ],
            "depends_on": ["FR-002"],
        },
        {
            "id": "FR-005",
            "type": "FR",
            "title": "Mock-оплата",
            "description": "Оплата имитируется: pending при старте, paid при завершении",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "При старте создаётся платёж в статусе pending",
                "При завершении статус меняется на paid с итоговой суммой",
            ],
            "depends_on": ["FR-002"],
        },
        {
            "id": "FR-006",
            "type": "FR",
            "title": "Admin-панель",
            "description": "Админ управляет зонами и тарифами, видит активные сессии",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "Админ создаёт/редактирует зону с тарифом",
                "Админ видит список активных сессий и историю по зоне",
            ],
            "depends_on": [],
        },
        {
            "id": "NFR-001",
            "type": "NFR",
            "title": "Время отклика",
            "description": "API отвечает не дольше 300 мс в 95% запросов",
            "priority": "should",
            "source": "customer",
            "acceptance_criteria": [],
            "depends_on": [],
        },
        {
            "id": "NFR-002",
            "type": "NFR",
            "title": "Безопасность",
            "description": "Доступ к админ-панели только для администратора; все операции аутентифицированы",
            "priority": "must",
            "source": "customer",
            "acceptance_criteria": [
                "Неавторизованный запрос к админ-API отклоняется",
                "Роль администратора проверяется на каждом запросе",
            ],
            "depends_on": [],
        },
    ],
    "constraints": [
        "MVP без реальной оплаты (mock)",
        "Мобильное приложение — Angular 20.1.6 (зафиксировано по PDF)",
        "Локальная корпоративная модель без доступа в интернет",
    ],
    "risks": [
        {"id": "RK-01", "text": "Геолокация неточна в плотной застройке", "impact": "Неверное определение зоны"},
        {"id": "RK-02", "text": "Таймеры уведомлений чувствительны к фону приложения", "impact": "Задержка уведомлений"},
    ],
    "assumptions": [
        "Водитель даёт согласие на геолокацию",
        "Одна активная сессия на водителя",
        "Тарифы задаются админом вручную",
        "Версия Angular зафиксирована как 20.1.6 (по PDF, ответ на Q-001)",
    ],
    "open_questions": [
        {
            "id": "Q-001",
            "text": "Какая версия Angular используется?",
            "severity": "blocking",
            "impact": "architecture",
            "options": ["17", "18", "19", "20.1.6"],
            "default_if_unanswered": "20.1.6",
        },
        {
            "id": "Q-002",
            "text": "Нужна ли поддержка нескольких парковочных зон в одной сессии?",
            "severity": "important",
            "impact": "architecture",
            "options": ["да", "нет"],
            "default_if_unanswered": "нет",
        },
    ],
}

# Ответ System Analysis-агента для демо-кейса.
SYSTEM_ANALYSIS_MOCK: dict[str, Any] = {
    "boundaries": {
        "inside": ["Управление сессиями", "Зоны и тарифы", "Уведомления", "Mock-оплата"],
        "outside": ["Геолокация устройства", "Планировщик уведомлений"],
    },
    "roles_permissions": [
        {"role": "Водитель", "permissions": ["Начать сессию", "Завершить сессию", "Смотреть историю"]},
        {"role": "Администратор", "permissions": ["Управлять зонами", "Управлять тарифами", "Смотреть сессии"]},
    ],
    "scenarios": [
        {
            "id": "US-001",
            "title": "Начало парковочной сессии",
            "actor": "Водитель",
            "requirement_ids": ["FR-001", "FR-002", "FR-005"],
            "steps": [
                "Водитель открывает приложение в платной зоне",
                "Система определяет зону и тариф",
                "Водитель нажимает «Начать сессию»",
                "Система создаёт сессию и платёж pending",
            ],
            "result": "Сессия активна, виден таймер и стоимость",
        },
        {
            "id": "US-002",
            "title": "Завершение сессии",
            "actor": "Водитель",
            "requirement_ids": ["FR-002", "FR-005"],
            "steps": [
                "Водитель нажимает «Завершить»",
                "Система фиксирует время окончания",
                "Платёж переводится в paid",
            ],
            "result": "Сессия завершена, итоговая стоимость показана",
        },
        {
            "id": "US-003",
            "title": "Просмотр истории",
            "actor": "Водитель",
            "requirement_ids": ["FR-004"],
            "steps": ["Водитель открывает «Историю»", "Система показывает список сессий"],
            "result": "История отсортирована по дате",
        },
        {
            "id": "US-004",
            "title": "Управление зонами",
            "actor": "Администратор",
            "requirement_ids": ["FR-006", "NFR-002"],
            "steps": [
                "Админ открывает панель",
                "Создаёт/редактирует зону и тариф",
                "Система проверяет права администратора",
            ],
            "result": "Зона сохранена, доступна водителям",
        },
    ],
    "entities": [
        {"name": "ParkingZone", "description": "Платная зона с тарифом"},
        {"name": "Session", "description": "Парковочная сессия водителя"},
        {"name": "Payment", "description": "Mock-платёж сессии"},
        {"name": "Notification", "description": "Уведомление водителю"},
    ],
    "assumptions": [
        "Одна активная сессия на водителя",
        "Тарифы задаются админом вручную",
        "Версия Angular зафиксирована как 20.1.6 (ответ на Q-001)",
    ],
    "open_questions": ["Поддержка нескольких зон в одной сессии (по умолчанию: нет)"],
}

# Ответ Architecture API-агента для демо-кейса.
ARCHITECTURE_MOCK: dict[str, Any] = {
    "entities": [
        {
            "name": "ParkingZone",
            "description": "Платная зона",
            "fields": [
                {"name": "id", "type": "string", "required": True, "description": "UUID"},
                {"name": "name", "type": "string", "required": True, "description": "Название"},
                {"name": "tariffPerHour", "type": "number", "required": True, "description": "Тариф"},
            ],
            "indexes": ["name"],
        },
        {
            "name": "Session",
            "description": "Парковочная сессия",
            "fields": [
                {"name": "id", "type": "string", "required": True, "description": "UUID"},
                {"name": "userId", "type": "string", "required": True, "description": "Водитель"},
                {"name": "zoneId", "type": "string", "required": True, "description": "Зона"},
                {"name": "startedAt", "type": "datetime", "required": True, "description": "Начало"},
                {"name": "endedAt", "type": "datetime", "required": False, "description": "Конец"},
                {"name": "status", "type": "string", "required": True, "description": "active/completed"},
            ],
            "indexes": ["userId", "status"],
        },
        {
            "name": "Payment",
            "description": "Mock-платёж",
            "fields": [
                {"name": "id", "type": "string", "required": True, "description": "UUID"},
                {"name": "sessionId", "type": "string", "required": True, "description": "Сессия"},
                {"name": "amount", "type": "number", "required": True, "description": "Сумма"},
                {"name": "status", "type": "string", "required": True, "description": "pending/paid"},
            ],
            "indexes": ["sessionId"],
        },
    ],
    "events": [
        {
            "name": "SessionStarted",
            "version": "1",
            "payload": {"sessionId": "string", "zoneId": "string", "startedAt": "datetime"},
            "idempotency_key": "sessionId",
            "description": "Сессия начата",
        },
        {
            "name": "SessionCompleted",
            "version": "1",
            "payload": {"sessionId": "string", "amount": "number", "endedAt": "datetime"},
            "idempotency_key": "sessionId",
            "description": "Сессия завершена",
        },
    ],
    "operations": [
        {
            "method": "get",
            "path": "/zones/{zoneId}",
            "operationId": "getZone",
            "summary": "Получить зону",
            "request_schema": None,
            "response_schema": {"$ref": "#/components/schemas/ParkingZone"},
            "errors": ["404"],
            "auth": False,
            "tags": ["zones"],
            "requirement_ids": ["FR-001"],
            "error_schema": "ProblemDetails",
        },
        {
            "method": "post",
            "path": "/sessions",
            "operationId": "startSession",
            "summary": "Начать сессию",
            "request_schema": {"type": "object", "properties": {"zoneId": {"type": "string"}}},
            "response_schema": {"$ref": "#/components/schemas/Session"},
            "errors": ["400", "409"],
            "auth": True,
            "tags": ["sessions"],
            "requirement_ids": ["FR-001", "FR-002", "FR-005"],
            "error_schema": "ProblemDetails",
        },
        {
            "method": "post",
            "path": "/sessions/{sessionId}/complete",
            "operationId": "completeSession",
            "summary": "Завершить сессию",
            "request_schema": None,
            "response_schema": {"$ref": "#/components/schemas/Session"},
            "errors": ["404"],
            "auth": True,
            "tags": ["sessions"],
            "requirement_ids": ["FR-002", "FR-005"],
            "error_schema": "ProblemDetails",
        },
        {
            "method": "get",
            "path": "/sessions",
            "operationId": "listSessions",
            "summary": "История сессий",
            "request_schema": None,
            "response_schema": {"type": "array", "items": {"$ref": "#/components/schemas/Session"}},
            "errors": [],
            "auth": True,
            "tags": ["sessions"],
            "requirement_ids": ["FR-004"],
            "error_schema": "ProblemDetails",
        },
        {
            "method": "post",
            "path": "/admin/zones",
            "operationId": "createZone",
            "summary": "Создать зону",
            "request_schema": {"type": "object", "properties": {"name": {"type": "string"}}},
            "response_schema": {"$ref": "#/components/schemas/ParkingZone"},
            "errors": ["400", "403"],
            "auth": True,
            "tags": ["admin", "zones"],
            "requirement_ids": ["FR-006", "NFR-002"],
            "error_schema": "ProblemDetails",
        },
    ],
}

# Ответ UI Design-агента для демо-кейса.
UI_MOCK: dict[str, Any] = {
    "flows": [
        {
            "id": "FLOW-001",
            "name": "Начало сессии",
            "steps": ["SCR-001", "SCR-002"],
        },
        {
            "id": "FLOW-002",
            "name": "История",
            "steps": ["SCR-003"],
        },
    ],
    "screens": [
        {
            "id": "SCR-001",
            "title": "Карта зоны",
            "requirement_ids": ["FR-001"],
            "states": {
                "empty": "Нет данных о зоне",
                "loading": "Определяем зону...",
                "error": "Ошибка геолокации",
                "forbidden": "",
                "success": "Зона определена",
            },
            "actions": [{"id": "ACT-001", "label": "Начать сессию", "api_operation_id": "startSession", "navigates_to": "SCR-002"}],
        },
        {
            "id": "SCR-002",
            "title": "Активная сессия",
            "requirement_ids": ["FR-002", "FR-003"],
            "states": {
                "empty": "",
                "loading": "Загрузка сессии...",
                "error": "Ошибка загрузки",
                "forbidden": "",
                "success": "Сессия активна",
            },
            "actions": [{"id": "ACT-002", "label": "Завершить", "api_operation_id": "completeSession", "navigates_to": "SCR-003"}],
        },
        {
            "id": "SCR-003",
            "title": "История",
            "requirement_ids": ["FR-004"],
            "states": {
                "empty": "Сессий пока нет",
                "loading": "Загрузка истории...",
                "error": "Ошибка загрузки",
                "forbidden": "",
                "success": "История загружена",
            },
            "actions": [{"id": "ACT-003", "label": "Обновить", "api_operation_id": "listSessions", "navigates_to": None}],
        },
    ],
    "components": [
        {"name": "SessionCard", "description": "Карточка сессии"},
        {"name": "ZoneMap", "description": "Карта зоны"},
    ],
}

# Реестр предзаданных ответов по имени этапа.
DEFAULT_MOCK_RESPONSES: dict[str, dict[str, Any]] = {
    "01_requirements": REQUIREMENTS_MOCK,
    "02_system_analysis": SYSTEM_ANALYSIS_MOCK,
    "03_architecture_api": ARCHITECTURE_MOCK,
    "04_ui_design": UI_MOCK,
}


class MockBackend:
    """Детерминированный источник ответов для режима ``LLM_MODE=mock``.

    Args:
        responses: Словарь «имя этапа -> JSON-ответ». Если не задан,
            используется общий реестр :data:`DEFAULT_MOCK_RESPONSES`.
    """

    def __init__(
        self,
        responses: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.responses = responses if responses is not None else DEFAULT_MOCK_RESPONSES

    def complete(
        self,
        stage: str,
        prompt_version: str,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Вернуть предзаданный ответ для этапа.

        Args:
            stage: Имя этапа.
            prompt_version: Версия промпта (не влияет на ответ).
            system_prompt: Системный промпт (игнорируется).
            user_prompt: Пользовательский промпт (игнорируется).
            json_schema: JSON Schema ответа (игнорируется).

        Returns:
            Предзаданный JSON-ответ.

        Raises:
            LLMUnavailable: Если для этапа нет предзаданного ответа.
        """
        try:
            return self.responses[stage]
        except KeyError:
            raise LLMUnavailable(
                f"MockLLM: нет предзаданного ответа для этапа {stage!r}; "
                "наполните реестр DEFAULT_MOCK_RESPONSES"
            ) from None
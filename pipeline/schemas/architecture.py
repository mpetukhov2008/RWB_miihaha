"""Схема артефакта «Архитектура и API» (ArchitectureApi).

Определяет модель данных, доменные события и операции API. OpenAPI-документ
строится детерминированно из ``operations`` (без LLM).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

HttpMethod = Literal["get", "post", "put", "patch", "delete"]


class EntityField(BaseModel):
    """Поле сущности модели данных.

    Attributes:
        name: Имя поля.
        type: Тип (string, integer, number, boolean, datetime, ...).
        required: Обязательность.
        description: Описание.
    """

    name: str
    type: str
    required: bool = False
    description: str = ""


class DataEntity(BaseModel):
    """Сущность модели данных.

    Attributes:
        name: Имя сущности.
        description: Описание.
        fields: Поля.
        indexes: Индексы.
    """

    name: str
    description: str = ""
    fields: list[EntityField] = Field(default_factory=list)
    indexes: list[str] = Field(default_factory=list)


class DomainEvent(BaseModel):
    """Доменное событие.

    Attributes:
        name: Имя события.
        version: Версия схемы события.
        payload: Пример payload (объект).
        idempotency_key: Ключ идемпотентности (опционально).
        description: Описание.
    """

    name: str
    version: str = "1"
    payload: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None
    description: str = ""


class ApiOperation(BaseModel):
    """Операция API.

    Attributes:
        method: HTTP-метод.
        path: Путь (например, ``/sessions``).
        operationId: Уникальный ID операции.
        summary: Краткое описание.
        request_schema: Схема тела запроса (JSON Schema-подобная).
        response_schema: Схема тела ответа.
        errors: Список кодов ошибок (HTTP).
        auth: Требуется ли аутентификация.
        tags: Теги OpenAPI.
        requirement_ids: Покрываемые требования (для трассируемости).
        error_schema: Имя единой схемы ошибок (``ProblemDetails``).
    """

    method: HttpMethod
    path: str
    operationId: str
    summary: str = ""
    request_schema: dict[str, Any] | None = None
    response_schema: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    auth: bool = False
    tags: list[str] = Field(default_factory=list)
    requirement_ids: list[str] = Field(default_factory=list)
    error_schema: str = "ProblemDetails"


class ArchitectureApi(BaseModel):
    """Артефакт этапа Architecture API.

    Attributes:
        entities: Модель данных.
        events: Доменные события.
        operations: Операции API.
    """

    entities: list[DataEntity] = Field(default_factory=list)
    events: list[DomainEvent] = Field(default_factory=list)
    operations: list[ApiOperation] = Field(default_factory=list)

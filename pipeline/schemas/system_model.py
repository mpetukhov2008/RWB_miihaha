"""Схема артефакта «Системная модель» (SystemAnalysis).

Определяет типизированную структуру ответа System Analysis-агента:
границы, роли/разрешения, сценарии, сущности, допущения и вопросы.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Boundary(BaseModel):
    """Границы системы.

    Attributes:
        inside: Что находится внутри системы.
        outside: Что находится снаружи (внешние системы, акторы).
    """

    inside: list[str] = Field(default_factory=list)
    outside: list[str] = Field(default_factory=list)


class RolePermission(BaseModel):
    """Роль и её разрешения.

    Attributes:
        role: Имя роли (из requirements.json).
        permissions: Список разрешений.
    """

    role: str
    permissions: list[str] = Field(default_factory=list)


class Scenario(BaseModel):
    """Сценарий использования.

    Attributes:
        id: Уникальный ID (``US-001`` и т.д.).
        title: Название сценария.
        actor: Актор (роль).
        requirement_ids: Покрываемые требования (must-FR).
        steps: Шаги сценария.
        result: Ожидаемый результат.
    """

    id: str = Field(pattern=r"^US-\d{3,}$")
    title: str
    actor: str
    requirement_ids: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    result: str = ""


class SystemEntity(BaseModel):
    """Сущность системы.

    Attributes:
        name: Имя сущности.
        description: Описание.
    """

    name: str
    description: str = ""


class SystemAnalysis(BaseModel):
    """Артефакт этапа System Analysis.

    Attributes:
        boundaries: Границы системы.
        roles_permissions: Роли и разрешения.
        scenarios: Сценарии использования.
        entities: Сущности.
        assumptions: Допущения системного уровня.
        open_questions: Открытые вопросы.
    """

    boundaries: Boundary = Field(default_factory=Boundary)
    roles_permissions: list[RolePermission] = Field(default_factory=list)
    scenarios: list[Scenario] = Field(default_factory=list)
    entities: list[SystemEntity] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
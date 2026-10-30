"""Схема артефакта «Требования» (RequirementsDoc).

Определяет типизированную структуру ответа Requirements-агента: цели, роли,
функциональные/нефункциональные требования, ограничения, риски, допущения
и открытые вопросы.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from pipeline.schemas.common import (
    QuestionId,
    RequirementId,
    RiskId,
    RoleId,
)


class Role(BaseModel):
    """Роль пользователя системы.

    Attributes:
        id: Уникальный ID роли (``R-`` + минимум 2 цифры).
        name: Название роли.
        description: Описание роли.
    """

    id: RoleId
    name: str
    description: str = ""


class Requirement(BaseModel):
    """Требование (функциональное FR или нефункциональное NFR).

    Attributes:
        id: Уникальный ID (``FR-``/``NFR-`` + минимум 3 цифры).
        type: Тип требования.
        title: Краткое название.
        description: Полное описание.
        priority: Приоритет: must/should/could.
        source: Источник: customer (от заказчика) или assumption (допущение).
        acceptance_criteria: Критерии приёмки.
        depends_on: ID требований, от которых зависит данное.
    """

    id: RequirementId
    type: Literal["FR", "NFR"]
    title: str
    description: str
    priority: Literal["must", "should", "could"]
    source: Literal["customer", "assumption"]
    acceptance_criteria: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)


class Risk(BaseModel):
    """Риск проекта.

    Attributes:
        id: Уникальный ID (``RK-`` + минимум 2 цифры).
        text: Описание риска.
        impact: Влияние риска.
    """

    id: RiskId
    text: str
    impact: str = ""


class Question(BaseModel):
    """Открытый вопрос к заказчику.

    Attributes:
        id: Уникальный ID (``Q-`` + минимум 3 цифры).
        text: Текст вопроса.
        severity: Важность: blocking/important/minor.
        impact: Область влияния: architecture/security/ux/other.
        options: Варианты ответа.
        default_if_unanswered: Значение по умолчанию, если не ответили.
    """

    id: QuestionId
    text: str
    severity: Literal["blocking", "important", "minor"] = "minor"
    impact: Literal["architecture", "security", "ux", "other"] = "other"
    options: list[str] = Field(default_factory=list)
    default_if_unanswered: str | None = None


class RequirementsDoc(BaseModel):
    """Артефакт этапа Requirements.

    Attributes:
        goals: Цели продукта.
        roles: Роли пользователей.
        requirements: Требования (FR и NFR).
        constraints: Ограничения.
        risks: Риски.
        assumptions: Допущения.
        open_questions: Открытые вопросы.
    """

    goals: list[str] = Field(default_factory=list)
    roles: list[Role] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[Question] = Field(default_factory=list)

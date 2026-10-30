"""Схема артефакта «UI-спецификация» (UiSpec).

Определяет экраны, состояния, действия и компоненты интерфейса.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ScreenStateName = Literal["empty", "loading", "error", "forbidden", "success"]


class UiAction(BaseModel):
    """Действие на экране.

    Attributes:
        id: Уникальный ID действия.
        label: Подпись.
        api_operation_id: Операция API (из openapi.yaml) или None.
        navigates_to: ID экрана, на который ведёт действие, или None.
    """

    id: str
    label: str
    api_operation_id: str | None = None
    navigates_to: str | None = None


class UiScreen(BaseModel):
    """Экран.

    Attributes:
        id: Уникальный ID (``SCR-001`` и т.д.).
        title: Заголовок.
        requirement_ids: Покрываемые требования.
        states: Состояния экрана ("empty"/"loading"/"error"/"forbidden"/"success").
        actions: Действия.
    """

    id: str = Field(pattern=r"^SCR-\d{3,}$")
    title: str
    requirement_ids: list[str] = Field(default_factory=list)
    states: dict[ScreenStateName, str] = Field(default_factory=dict)
    actions: list[UiAction] = Field(default_factory=list)


class UiFlow(BaseModel):
    """Пользовательский поток.

    Attributes:
        id: Уникальный ID (``FLOW-001`` и т.д.).
        name: Название потока.
        steps: Последовательность экранов/действий.
    """

    id: str = Field(pattern=r"^FLOW-\d{3,}$")
    name: str
    steps: list[str] = Field(default_factory=list)


class UiComponent(BaseModel):
    """Переиспользуемый компонент.

    Attributes:
        name: Имя компонента.
        description: Описание.
    """

    name: str
    description: str = ""


class UiSpec(BaseModel):
    """Артефакт этапа UI Design.

    Attributes:
        flows: Пользовательские потоки.
        screens: Экраны.
        components: Компоненты.
    """

    flows: list[UiFlow] = Field(default_factory=list)
    screens: list[UiScreen] = Field(default_factory=list)
    components: list[UiComponent] = Field(default_factory=list)
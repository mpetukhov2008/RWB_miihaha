"""Общие Pydantic-модели пайплайна (ID, приоритеты, severity)."""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import Field

# ID-паттерны по фазам. Применяются через Field(pattern=...) в Annotated,
# чтобы модель не позволяла создать объект с неверным ID.
ID_PATTERN_REQUIREMENT = r"^(FR|NFR)-\d{3,}$"
ID_PATTERN_ROLE = r"^R-\d{2,}$"
ID_PATTERN_RISK = r"^RK-\d{2,}$"
ID_PATTERN_QUESTION = r"^Q-\d{3,}$"
ID_PATTERN_SCREEN = r"^SCR-\d{3,}$"

RequirementId = Annotated[str, Field(pattern=ID_PATTERN_REQUIREMENT)]
RoleId = Annotated[str, Field(pattern=ID_PATTERN_ROLE)]
RiskId = Annotated[str, Field(pattern=ID_PATTERN_RISK)]
QuestionId = Annotated[str, Field(pattern=ID_PATTERN_QUESTION)]
ScreenId = Annotated[str, Field(pattern=ID_PATTERN_SCREEN)]


def is_valid_id(value: str, pattern: str) -> bool:
    """Проверить, что строка соответствует ID-паттерну.

    Args:
        value: Проверяемая строка.
        pattern: Регулярное выражение.

    Returns:
        ``True``, если строка полностью соответствует паттерну.
    """
    return re.fullmatch(pattern, value) is not None
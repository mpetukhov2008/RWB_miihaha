"""Загрузка промптов из ``prompts/{stage}/{version}.md``."""

from __future__ import annotations

from pipeline.config import PROMPTS_DIR


def load_prompt(stage: str, version: str) -> str:
    """Прочитать системный промпт этапа.

    Args:
        stage: Имя этапа (например, ``requirements``).
        version: Версия промпта (например, ``v1``).

    Returns:
        Содержимое файла промпта.

    Raises:
        FileNotFoundError: Если файл промпта отсутствует.
    """
    path = PROMPTS_DIR / stage / f"{version}.md"
    return path.read_text(encoding="utf-8")
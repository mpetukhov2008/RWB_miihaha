"""Загрузка промптов из ``pipeline/agents/{stage}/prompt.md``.

Каждый агент (этап) — директория с `prompt.md`, `schema.json`, `checklist.md`.
Версия промпта задаётся агентом (``prompt_version``) и фиксируется в state.json.
"""

from __future__ import annotations

from pipeline.config import PROMPTS_DIR


def load_prompt(stage: str, version: str = "v1") -> str:
    """Прочитать системный промпт этапа.

    Args:
        stage: Имя этапа — имя директории агента (например, ``01_requirements``).
        version: Версия промпта. Файлы именуются `prompt.md` (текущая версия)
            или `prompt_{version}.md` (конкретная версия).

    Returns:
        Содержимое файла промпта.

    Raises:
        FileNotFoundError: Если файл промпта отсутствует.
    """
    dir_path = PROMPTS_DIR / stage
    if version == "v1":
        path = dir_path / "prompt.md"
    else:
        path = dir_path / f"prompt_{version}.md"
    return path.read_text(encoding="utf-8")
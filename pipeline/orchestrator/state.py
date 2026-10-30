"""Состояние прогона: ``state.json`` в корне ``runs/{run_id}/``.

Хранит статус каждого этапа и версию промпта. Позволяет возобновлять прогон:
этапы со статусом ``done`` пропускаются.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class RunState:
    """Чтение/запись ``state.json`` прогона.

    Args:
        run_dir: Корень прогона (``runs/{run_id}/``).
    """

    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        run_dir.mkdir(parents=True, exist_ok=True)
        self.path = run_dir / "state.json"
        self.data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        """Прочитать state.json; при отсутствии — пустое состояние."""
        if not self.path.exists():
            return {"run_id": self.run_dir.name, "stages": {}, "created_at": self._now()}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"run_id": self.run_dir.name, "stages": {}, "created_at": self._now()}

    @staticmethod
    def _now() -> str:
        """Текущее время в UTC ISO 8601."""
        return datetime.now(UTC).isoformat()

    def save(self) -> None:
        """Записать состояние на диск."""
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def stage_status(self, stage: str) -> str:
        """Статус этапа.

        Args:
            stage: Имя этапа.

        Returns:
            Один из: ``pending``/``running``/``done``/``failed``/
            ``waiting_answers``.
        """
        return self.data["stages"].get(stage, {}).get("status", "pending")

    def start_stage(self, stage: str, prompt_version: str) -> None:
        """Отметить этап как выполняющийся.

        Args:
            stage: Имя этапа.
            prompt_version: Версия промпта.
        """
        self.data["stages"][stage] = {
            "status": "running",
            "prompt_version": prompt_version,
            "started_at": self._now(),
        }
        self.save()

    def finish_stage(self, stage: str, gates: dict[str, str]) -> None:
        """Отметить этап завершённым с результатами gates.

        Args:
            stage: Имя этапа.
            gates: Словарь «имя gate -> ok/fail».
        """
        self.data["stages"][stage].update(
            {
                "status": "done",
                "gates": gates,
                "finished_at": self._now(),
            }
        )
        self.save()

    def fail_stage(self, stage: str, reason: str) -> None:
        """Отметить этап упавшим.

        Args:
            stage: Имя этапа.
            reason: Причина ошибки.
        """
        self.data["stages"][stage].update(
            {
                "status": "failed",
                "error": reason,
                "failed_at": self._now(),
            }
        )
        self.save()

    def wait_answers(self, stage: str) -> None:
        """Перевести этап в ожидание ответов на blocking-вопросы.

        Args:
            stage: Имя этапа.
        """
        self.data["stages"][stage].update(
            {
                "status": "waiting_answers",
                "waiting_since": self._now(),
            }
        )
        self.save()
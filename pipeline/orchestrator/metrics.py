"""Метрики прогона: агрегация логов LLM в ``reports/usage.json``.

После прогона читает ``logs/agent-calls.jsonl`` и ``state.json`` и строит
сводный отчёт по токенам, времени, вызовам и retry.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def build_usage_report(run_dir: Path) -> dict[str, Any]:
    """Собрать сводный отчёт по прогону.

    Args:
        run_dir: Корень прогона (``generated/<case>/``).

    Returns:
        Словарь с полями: ``total_time_sec``, ``total_tokens_in``,
        ``total_tokens_out``, ``calls``, ``retries``, ``cache_hits``,
        ``stages_first_try_ok``, ``stages_total``, ``manual_edits``,
        ``per_stage``.
    """
    calls: list[dict[str, Any]] = []
    log_path = run_dir / "logs" / "agent-calls.jsonl"
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                calls.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("Битая строка лога: %s", line)

    total_tokens_in = sum(c.get("tokens_in", 0) for c in calls)
    total_tokens_out = sum(c.get("tokens_out", 0) for c in calls)
    total_latency_ms = sum(c.get("latency_ms", 0) for c in calls)
    cache_hits = sum(1 for c in calls if c.get("status") == "cache_hit")
    # Retry: вызовы одного этапа с attempt > 1.
    retries = sum(1 for c in calls if c.get("attempt", 1) > 1)

    per_stage: dict[str, dict[str, Any]] = {}
    for c in calls:
        stage = c.get("stage", "unknown")
        entry = per_stage.setdefault(
            stage,
            {"calls": 0, "tokens_in": 0, "tokens_out": 0, "latency_ms": 0, "cache_hits": 0},
        )
        entry["calls"] += 1
        entry["tokens_in"] += c.get("tokens_in", 0)
        entry["tokens_out"] += c.get("tokens_out", 0)
        entry["latency_ms"] += c.get("latency_ms", 0)
        if c.get("status") == "cache_hit":
            entry["cache_hits"] += 1

    # Статусы этапов из state.json.
    stages_total = 0
    stages_first_try_ok = 0
    state_path = run_dir / "state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            stages = state.get("stages", {})
            stages_total = len(stages)
            stages_first_try_ok = sum(
                1
                for s in stages.values()
                if s.get("status") == "done" and s.get("gates")
                and all(v == "ok" for v in s["gates"].values())
            )
        except (json.JSONDecodeError, OSError):
            logger.warning("Не удалось прочитать state.json: %s", state_path)

    return {
        "total_time_sec": round(total_latency_ms / 1000, 3),
        "total_tokens_in": total_tokens_in,
        "total_tokens_out": total_tokens_out,
        "calls": len(calls),
        "retries": retries,
        "cache_hits": cache_hits,
        "stages_first_try_ok": stages_first_try_ok,
        "stages_total": stages_total,
        "manual_edits": 0,
        "per_stage": per_stage,
    }


def write_usage_report(run_dir: Path) -> Path:
    """Записать ``reports/usage.json`` прогона.

    Args:
        run_dir: Корень прогона.

    Returns:
        Путь к записанному файлу.
    """
    report = build_usage_report(run_dir)
    out = run_dir / "reports" / "usage.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
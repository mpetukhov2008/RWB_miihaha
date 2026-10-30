"""Трассируемость: требование → API → экран → тест.

Читает артефакты прогона и строит матрицу ``reports/traceability.json``
и человекочитаемый ``reports/traceability.md``.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def _read_json(path: Path) -> Any:
    """Прочитать JSON; при ошибке — None."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def build_traceability(run_dir: Path) -> dict[str, dict[str, list[str]]]:
    """Построить матрицу трассируемости.

    Args:
        run_dir: Корень прогона.

    Returns:
        Словарь «FR-XXX -> {api: [...], ui: [...], tests: [...], docs: [...]}».
    """
    requirements = _read_json(run_dir / "01_requirements" / "requirements.json") or {}
    ui_spec = _read_json(run_dir / "04_ui_design" / "ui-spec.json") or {}
    api_tests = _read_json(run_dir / "07_tests" / "api-tests.json") or []

    api_ops: list[dict[str, Any]] = []
    openapi_path = run_dir / "03_architecture_api" / "openapi.yaml"
    if openapi_path.exists():
        try:
            openapi = yaml.safe_load(openapi_path.read_text(encoding="utf-8")) or {}
            for path_item in (openapi.get("paths") or {}).values():
                for _method, op in path_item.items():
                    if isinstance(op, dict) and "operationId" in op:
                        api_ops.append(op)
        except Exception:  # noqa: BLE001
            logger.warning("Не удалось прочитать openapi.yaml")

    trace: dict[str, dict[str, list[str]]] = {}
    for req in requirements.get("requirements", []):
        rid = req.get("id")
        if not rid:
            continue
        api = [
            op["operationId"]
            for op in api_ops
            if rid in (op.get("x-requirement-ids") or [])
        ]
        ui = [
            s["id"]
            for s in ui_spec.get("screens", [])
            if rid in (s.get("requirement_ids") or [])
        ]
        tests = [
            f"{t.get('method', '').upper()} {t.get('path', '')}"
            for t in api_tests
            if rid in (t.get("requirement_ids") or [])
        ] + [
            t.get("name", "")
            for t in (_read_json(run_dir / "07_tests" / "e2e-tests.json") or [])
            if rid == t.get("scenario_id")
        ]
        docs: list[str] = []
        guide = run_dir / "09_docs" / "docs" / "user-guide.md"
        if guide.exists() and rid in guide.read_text(encoding="utf-8"):
            docs.append("docs/user-guide.md")

        trace[rid] = {"api": api, "ui": ui, "tests": tests, "docs": docs}

    return trace


def write_traceability(run_dir: Path) -> tuple[Path, Path]:
    """Записать traceability.json и traceability.md.

    Args:
        run_dir: Корень прогона.

    Returns:
        Кортеж путей (json, md).
    """
    trace = build_traceability(run_dir)

    json_path = run_dir / "reports" / "traceability.json"
    md_path = run_dir / "reports" / "traceability.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Traceability", "", "| Требование | API | UI | Tests | Docs |", "|---|---|---|---|---|"]
    for rid, row in trace.items():
        lines.append(
            f"| {rid} | {', '.join(row['api']) or '—'} | "
            f"{', '.join(row['ui']) or '—'} | {', '.join(row['tests']) or '—'} | "
            f"{', '.join(row['docs']) or '—'} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
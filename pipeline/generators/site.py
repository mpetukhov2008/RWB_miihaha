"""Детерминированная генерация статического сайта из артефактов прогона.

Собирает HTML-сайт в ``generated/<case>/site/`` из артефактов этапов
01–09: требования, OpenAPI, модель данных, UI-экраны, трассируемость,
отчёты. Без LLM. Все данные экранируются (html.escape).
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import yaml

_STAGE_TITLES = {
    "01_requirements": "Требования",
    "02_system_analysis": "Системный анализ",
    "03_architecture_api": "Архитектура и API",
    "04_ui_design": "Дизайн интерфейса",
    "05_codegen_backend": "Backend",
    "06_codegen_frontend": "Frontend",
    "07_tests": "Тесты",
    "08_security_report": "Безопасность",
    "09_docs": "Документация",
}

_STYLE = """\
body { font-family: system-ui, sans-serif; margin: 0; color: #1a1a2e; }
header { background: #1976d2; color: #fff; padding: 16px 24px; }
header h1 { margin: 0; font-size: 1.4rem; }
nav { background: #eee; padding: 8px 24px; }
nav a { margin-right: 16px; color: #1976d2; text-decoration: none; }
main { max-width: 960px; margin: 0 auto; padding: 16px 24px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
th { background: #f5f5f5; }
code, pre { background: #f5f5f5; font-size: 0.9em; }
pre { padding: 10px; overflow-x: auto; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
.ok { background: #c8e6c9; } .fail { background: #ffcdd2; }"""


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _esc(value: Any) -> str:
    return html.escape(str(value))


def _page(title: str, nav: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(title)}</title>
<style>{_STYLE}</style>
</head>
<body>
<header><h1>{_esc(title)}</h1></header>
<nav>{nav}</nav>
<main>{body}</main>
</body>
</html>
"""


def _nav(case_name: str) -> str:
    links = [f'<a href="index.html">{_esc(case_name)}</a>']
    for slug, title in (
        ("requirements.html", "Требования"),
        ("api.html", "API"),
        ("data-model.html", "Модель данных"),
        ("ui.html", "Экраны"),
        ("traceability.html", "Трассируемость"),
        ("reports.html", "Отчёты"),
    ):
        links.append(f'<a href="{slug}">{title}</a>')
    return "".join(links)


def _requirements_page(run_dir: Path, case_name: str) -> str:
    req = _read_json(run_dir / "01_requirements" / "requirements.json") or {}
    rows = []
    for r in req.get("requirements") or []:
        rows.append(
            f"<tr><td><code>{_esc(r.get('id', ''))}</code></td>"
            f"<td>{_esc(r.get('title', ''))}</td>"
            f"<td>{_esc(r.get('priority', ''))}</td></tr>"
        )
    body = f"<h2>Функциональные требования</h2>"
    if rows:
        body += '<table><tr><th>ID</th><th>Название</th><th>Приоритет</th></tr>' + "".join(rows) + "</table>"
    else:
        body += "<p>Требования не найдены.</p>"
    return _page(f"{case_name} — Требования", _nav(case_name), body)


def _api_page(run_dir: Path, case_name: str) -> str:
    openapi_path = run_dir / "03_architecture_api" / "openapi.yaml"
    rows = []
    if openapi_path.exists():
        try:
            openapi = yaml.safe_load(openapi_path.read_text(encoding="utf-8")) or {}
            for path_item, methods in (openapi.get("paths") or {}).items():
                for method, op in methods.items():
                    if isinstance(op, dict) and "operationId" in op:
                        auth = "🔒" if op.get("security") else ""
                        rows.append(
                            f"<tr><td><code>{_esc(method.upper())}</code></td>"
                            f"<td><code>{_esc(path_item)}</code></td>"
                            f"<td>{_esc(op.get('summary', ''))} {auth}</td>"
                            f"<td><code>{_esc(op.get('operationId', ''))}</code></td></tr>"
                        )
        except Exception:  # noqa: BLE001
            rows.append('<tr><td colspan="4">Ошибка чтения openapi.yaml</td></tr>')
    body = "<h2>Операции API</h2>"
    if rows:
        body += (
            '<table><tr><th>Метод</th><th>Путь</th><th>Описание</th><th>operationId</th></tr>'
            + "".join(rows)
            + "</table>"
        )
    else:
        body += "<p>OpenAPI не найден.</p>"
    return _page(f"{case_name} — API", _nav(case_name), body)


def _data_model_page(run_dir: Path, case_name: str) -> str:
    model = _read_json(run_dir / "03_architecture_api" / "data-model.json") or {}
    sections = []
    for ent in model.get("entities") or []:
        rows = "".join(
            f"<tr><td><code>{_esc(f.get('name', ''))}</code></td>"
            f"<td>{_esc(f.get('type', ''))}</td>"
            f"<td>{'да' if f.get('required') else '—'}</td></tr>"
            for f in ent.get("fields") or []
        )
        sections.append(
            f"<h3>{_esc(ent.get('name', ''))}</h3>"
            f"<table><tr><th>Поле</th><th>Тип</th><th>Обязательное</th></tr>{rows}</table>"
        )
    body = "<h2>Модель данных</h2>" + ("".join(sections) or "<p>Модель пуста.</p>")
    return _page(f"{case_name} — Модель данных", _nav(case_name), body)


def _ui_page(run_dir: Path, case_name: str) -> str:
    ui = _read_json(run_dir / "04_ui_design" / "ui-spec.json") or {}
    cards = []
    for s in ui.get("screens") or []:
        actions = ", ".join(_esc(a.get("label", "")) for a in s.get("actions") or [])
        cards.append(
            f"<h3>{_esc(s.get('id', ''))}: {_esc(s.get('title', ''))}</h3>"
            f"<p>Действия: {actions or '—'}</p>"
        )
    body = "<h2>Экраны интерфейса</h2>" + ("".join(cards) or "<p>Экраны не найдены.</p>")
    return _page(f"{case_name} — Экраны", _nav(case_name), body)


def _traceability_page(run_dir: Path, case_name: str) -> str:
    trace = _read_json(run_dir / "reports" / "traceability.json") or {}
    rows = "".join(
        f"<tr><td><code>{_esc(rid)}</code></td>"
        f"<td>{_esc(', '.join(row.get('api') or []) or '—')}</td>"
        f"<td>{_esc(', '.join(row.get('ui') or []) or '—')}</td>"
        f"<td>{_esc(', '.join(row.get('tests') or []) or '—')}</td></tr>"
        for rid, row in trace.items()
    )
    body = "<h2>Матрица трассируемости</h2>"
    if rows:
        body += (
            '<table><tr><th>Требование</th><th>API</th><th>UI</th><th>Тесты</th></tr>'
            + rows
            + "</table>"
        )
    else:
        body += "<p>Матрица не построена.</p>"
    return _page(f"{case_name} — Трассируемость", _nav(case_name), body)


def _reports_page(run_dir: Path, case_name: str) -> str:
    usage = _read_json(run_dir / "reports" / "usage.json") or {}
    state = _read_json(run_dir / "state.json") or {}
    stage_rows = []
    for stage, info in (state.get("stages") or {}).items():
        status = info.get("status", "") if isinstance(info, dict) else ""
        badge = "ok" if status == "done" else "fail"
        title = _STAGE_TITLES.get(stage, stage)
        stage_rows.append(
            f"<tr><td>{_esc(title)}</td>"
            f'<td><span class="badge {badge}">{_esc(status)}</span></td></tr>'
        )
    usage_rows = "".join(
        f"<tr><td>{_esc(k)}</td><td><code>{_esc(v)}</code></td></tr>"
        for k, v in usage.items()
        if not isinstance(v, (dict, list))
    )
    security_md = _read_text(run_dir / "08_security_report" / "reports" / "security-report.md")
    body = (
        "<h2>Статусы этапов</h2>"
        + ('<table><tr><th>Этап</th><th>Статус</th></tr>' + "".join(stage_rows) + "</table>" if stage_rows else "<p>Состояние отсутствует.</p>")
        + "<h2>Метрики прогона</h2>"
        + ('<table><tr><th>Показатель</th><th>Значение</th></tr>' + usage_rows + "</table>" if usage_rows else "")
        + "<h2>Отчёт безопасности</h2>"
        + (f"<pre>{_esc(security_md)}</pre>" if security_md else "<p>Отчёт отсутствует.</p>")
    )
    return _page(f"{case_name} — Отчёты", _nav(case_name), body)


def _index_page(run_dir: Path, case_name: str) -> str:
    state = _read_json(run_dir / "state.json") or {}
    done = sum(
        1
        for info in (state.get("stages") or {}).values()
        if isinstance(info, dict) and info.get("status") == "done"
    )
    total = len(state.get("stages") or {})
    cards = []
    for stage, title in _STAGE_TITLES.items():
        status = (state.get("stages") or {}).get(stage, {})
        status_str = status.get("status", "—") if isinstance(status, dict) else "—"
        badge = "ok" if status_str == "done" else "fail"
        cards.append(
            f'<tr><td>{_esc(title)}</td><td><code>{_esc(stage)}</code></td>'
            f'<td><span class="badge {badge}">{_esc(status_str)}</span></td></tr>'
        )
    body = (
        f"<h2>Прогон: {_esc(case_name)}</h2>"
        f"<p>Этапов завершено: <strong>{done} из {total}</strong></p>"
        "<h2>Этапы</h2>"
        '<table><tr><th>Этап</th><th>Каталог</th><th>Статус</th></tr>'
        + "".join(cards)
        + "</table>"
    )
    return _page(f"Пайплайн: {case_name}", _nav(case_name), body)


def build_site(run_dir: Path) -> dict[str, str]:
    """Собрать статический сайт из артефактов прогона.

    Args:
        run_dir: Корень прогона (``generated/<case>/``).

    Returns:
        Словарь «имя файла -> HTML» (относительно ``site/``).
    """
    case_name = run_dir.name
    pages = {
        "index.html": _index_page(run_dir, case_name),
        "requirements.html": _requirements_page(run_dir, case_name),
        "api.html": _api_page(run_dir, case_name),
        "data-model.html": _data_model_page(run_dir, case_name),
        "ui.html": _ui_page(run_dir, case_name),
        "traceability.html": _traceability_page(run_dir, case_name),
        "reports.html": _reports_page(run_dir, case_name),
    }
    return pages


def write_site(run_dir: Path) -> Path:
    """Сгенерировать сайт и записать в ``<run_dir>/site/``.

    Args:
        run_dir: Корень прогона.

    Returns:
        Путь к каталогу сайта.
    """
    site_dir = run_dir / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in build_site(run_dir).items():
        (site_dir / filename).write_text(content, encoding="utf-8")
    return site_dir

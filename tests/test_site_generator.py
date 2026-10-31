"""Тесты генератора статического сайта."""

from __future__ import annotations

from pipeline.generators.site import build_site, write_site

RUN_STATE = {
    "stages": {
        "01_requirements": {"status": "done"},
        "02_system_analysis": {"status": "done"},
        "05_codegen_backend": {"status": "failed"},
    }
}

OPENAPI = """
openapi: 3.1.0
info:
  title: Demo
  version: 1.0.0
paths:
  /sessions:
    post:
      operationId: startSession
      summary: Начать сессию
      security:
        - bearerAuth: []
"""


def _prepare(tmp_path):
    (tmp_path / "01_requirements").mkdir()
    (tmp_path / "01_requirements" / "requirements.json").write_text(
        '{"requirements": [{"id": "FR-001", "title": "Вход <по логину>", "priority": "must"}]}',
        encoding="utf-8",
    )
    (tmp_path / "03_architecture_api").mkdir()
    (tmp_path / "03_architecture_api" / "openapi.yaml").write_text(OPENAPI, encoding="utf-8")
    (tmp_path / "04_ui_design").mkdir()
    (tmp_path / "04_ui_design" / "ui-spec.json").write_text(
        '{"screens": [{"id": "SCR-001", "title": "Вход", '
        '"actions": [{"label": "Отправить"}]}]}',
        encoding="utf-8",
    )
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "usage.json").write_text(
        '{"total_tokens_in": 100, "calls": 9}', encoding="utf-8"
    )
    (tmp_path / "reports" / "traceability.json").write_text(
        '{"FR-001": {"api": ["startSession"], "ui": ["SCR-001"], "tests": []}}',
        encoding="utf-8",
    )
    (tmp_path / "state.json").write_text(
        '{"stages": ' + str(RUN_STATE["stages"]).replace("'", '"') + "}",
        encoding="utf-8",
    )


def test_build_site_creates_all_pages(tmp_path) -> None:
    _prepare(tmp_path)
    pages = build_site(tmp_path)

    assert set(pages) == {
        "index.html",
        "requirements.html",
        "api.html",
        "data-model.html",
        "ui.html",
        "traceability.html",
        "reports.html",
    }
    assert "startSession" in pages["api.html"]
    assert "SCR-001" in pages["ui.html"]
    assert "FR-001" in pages["traceability.html"]
    assert "2 из 3" in pages["index.html"]


def test_site_escapes_html_in_data(tmp_path) -> None:
    _prepare(tmp_path)
    pages = build_site(tmp_path)

    assert "Вход &lt;по логину&gt;" in pages["requirements.html"]
    assert "Вход <по логину>" not in pages["requirements.html"]


def test_write_site_creates_directory(tmp_path) -> None:
    _prepare(tmp_path)
    site_dir = write_site(tmp_path)

    assert (site_dir / "index.html").exists()
    assert (site_dir / "api.html").exists()
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert html.startswith("<!doctype html>")
    assert "</html>" in html


def test_empty_run_produces_valid_pages(tmp_path) -> None:
    pages = build_site(tmp_path)

    assert "Требования не найдены" in pages["requirements.html"]
    assert "OpenAPI не найден" in pages["api.html"]
    assert "0 из 0" in pages["index.html"]


def test_generation_is_deterministic(tmp_path) -> None:
    _prepare(tmp_path)
    first = build_site(tmp_path)
    second = build_site(tmp_path)

    assert first == second

"""CLI пайплайна на typer.

Команда ``pipeline run`` создаёт результат в ``generated/<case>/``
(или ``runs/{run_id}/``, если передан ``--run-id``), читает бизнес-требования
(и, опционально, ответы на blocking-вопросы) и запускает оркестратор по этапам.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import typer

from pipeline import __version__
from pipeline.config import GENERATED_DIR, RUN_ID_FORMAT, RUNS_DIR, Settings, load_env

app = typer.Typer(
    name="pipeline",
    help="Универсальный ИИ-пайплайн разработки",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    """Печать версии и выход при ``--version``."""
    if value:
        typer.echo(f"pipeline {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        help="Показать версию и выйти",
    ),
) -> None:
    """Точка входа CLI: загружает env перед выполнением команд."""
    load_env()


@app.command()
def run(
    requirements: Path = typer.Option(
        ...,
        "--requirements",
        "-r",
        exists=True,
        dir_okay=False,
        help="Путь к файлу с бизнес-требованиями (markdown)",
    ),
    answers: Path | None = typer.Option(
        None,
        "--answers",
        "-a",
        exists=True,
        dir_okay=False,
        help="Путь к JSON с ответами на blocking-вопросы",
    ),
    run_id: str = typer.Option(
        "",
        "--run-id",
        help="Идентификатор прогона; по умолчанию — generated/<кейс>/",
    ),
) -> None:
    """Запустить пайплайн: требования -> ... -> документация.

    Результат пишется в ``generated/<кейс>/`` (самодостаточный набор
    артефактов и кода). При остановке на blocking-вопросах печатает в stderr
    путь к ожидаемому ``answers.json`` и завершается с кодом 2.
    """
    settings = Settings()
    rid = run_id or datetime.now().strftime(RUN_ID_FORMAT)

    # Определяем директорию прогона: generated/<case>/ по умолчанию.
    case_name = requirements.parent.name if requirements.parent.name != "." else "default"
    out_dir = GENERATED_DIR / case_name
    if run_id:
        out_dir = RUNS_DIR / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    requirements_md = requirements.read_text(encoding="utf-8")
    answers_data: dict[str, str] | None = None
    if answers is not None:
        answers_data = json.loads(answers.read_text(encoding="utf-8"))

    # Оркестратор подключается намеренно здесь, а не на уровне модуля,
    # чтобы `pipeline --help` работал без установленных зависимостей LLM.
    from pipeline.orchestrator.orchestrator import run_pipeline

    result = run_pipeline(
        run_dir=out_dir,
        requirements_md=requirements_md,
        answers=answers_data,
        settings=settings,
    )

    if result == "waiting_answers":
        typer.echo(
            f"Ожидание answers.json -> {out_dir / 'answers.json'}",
            err=True,
        )
        raise typer.Exit(code=2)

    typer.echo(f"Пайплайн завершён. Результат: {out_dir}")
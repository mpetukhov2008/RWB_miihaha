"""CLI пайплайна на typer.

Команда ``pipeline run`` создаёт директорию прогона ``runs/{run_id}/``,
читает бизнес-требования (и, опционально, ответы на blocking-вопросы)
и запускает оркестратор по этапам.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import typer

from pipeline import __version__
from pipeline.config import RUN_ID_FORMAT, RUNS_DIR, Settings, load_env

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
        help="Идентификатор прогона; по умолчанию — текущая метка времени",
    ),
) -> None:
    """Запустить пайплайн: требования -> системная модель -> UI -> документация.

    При остановке на blocking-вопросах печатает в stderr путь к ожидаемому
    ``answers.json`` и завершается с кодом 2.
    """
    rid = run_id or datetime.now().strftime(RUN_ID_FORMAT)
    run_dir = RUNS_DIR / rid
    run_dir.mkdir(parents=True, exist_ok=True)

    requirements_md = requirements.read_text(encoding="utf-8")
    answers_data: dict[str, str] | None = None
    if answers is not None:
        answers_data = json.loads(answers.read_text(encoding="utf-8"))

    # Оркестратор подключается намеренно здесь, а не на уровне модуля,
    # чтобы `pipeline --help` работал без установленных зависимостей LLM.
    from pipeline.pipeline.orchestrator import run_pipeline

    result = run_pipeline(
        run_dir=run_dir,
        requirements_md=requirements_md,
        answers=answers_data,
        settings=Settings(),
    )

    if result == "waiting_answers":
        typer.echo(
            f"Ожидание answers.json -> {run_dir / 'answers.json'}",
            err=True,
        )
        raise typer.Exit(code=2)

    typer.echo(f"Пайплайн завершён. Артефакты: {run_dir}")


if __name__ == "__main__":
    sys.exit(app())
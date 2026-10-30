"""Цикл самоисправления сборки (build_fix_loop).

Сборка → разбор ошибок компилятора → агент правит ТОЛЬКО проблемный
файл → повтор. Лимит попыток N; при провале проблема попадает в отчёт,
прогон идёт дальше. Счётчики попыток и токенов отдаются в отчёт
эффективности (см. reports/usage.json).

Модуль детерминированный и не зависит от LLM: функция исправления
(``fixer``) и запуск сборки (``build``) передаются снаружи. В тестах
используются заглушки, в пайплайне — реальный агент и команды сборки.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

_CS_ERROR_RE = re.compile(
    r"^(?P<path>[^(\s]+)\((?P<line>\d+)(?:,\d+)?\): error (?P<code>CS\d+): (?P<msg>.+)$"
)


@dataclass(frozen=True)
class CompilerError:
    path: str
    line: int
    code: str
    message: str


@dataclass
class BuildFixReport:
    success: bool
    attempts: int
    tokens_in: int = 0
    tokens_out: int = 0
    fixed_files: list[str] = field(default_factory=list)
    remaining_errors: list[CompilerError] = field(default_factory=list)


def parse_compiler_errors(log: str) -> list[CompilerError]:
    errors: list[CompilerError] = []
    for raw in log.splitlines():
        match = _CS_ERROR_RE.match(raw.strip())
        if match:
            errors.append(
                CompilerError(
                    path=match.group("path").replace("\\", "/"),
                    line=int(match.group("line")),
                    code=match.group("code"),
                    message=match.group("msg"),
                )
            )
    return errors


BuildFn = Callable[[dict[str, str]], tuple[bool, str]]

FixFn = Callable[[str, str, CompilerError], tuple[str, int, int]]


class BuildFixLoop:
    def __init__(self, build: BuildFn, fixer: FixFn, max_attempts: int = 3) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        self._build = build
        self._fixer = fixer
        self._max_attempts = max_attempts

    def run(self, files: dict[str, str]) -> BuildFixReport:
        current = dict(files)
        tokens_in = tokens_out = 0
        fixed: list[str] = []

        for attempt in range(1, self._max_attempts + 1):
            ok, log = self._build(current)
            if ok:
                return BuildFixReport(
                    success=True,
                    attempts=attempt,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    fixed_files=fixed,
                )
            errors = parse_compiler_errors(log)
            if not errors:
                return BuildFixReport(
                    success=False,
                    attempts=attempt,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    fixed_files=fixed,
                    remaining_errors=[],
                )

            error = next((e for e in errors if e.path in current), None)
            if error is None:
                return BuildFixReport(
                    success=False,
                    attempts=attempt,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    fixed_files=fixed,
                    remaining_errors=errors,
                )

            new_content, t_in, t_out = self._fixer(error.path, current[error.path], error)
            tokens_in += t_in
            tokens_out += t_out
            if new_content != current[error.path] and error.path not in fixed:
                fixed.append(error.path)
            current[error.path] = new_content

        _, log = self._build(current)
        remaining = parse_compiler_errors(log)
        return BuildFixReport(
            success=not remaining,
            attempts=self._max_attempts,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            fixed_files=fixed,
            remaining_errors=remaining,
        )

"""Тесты цикла самоисправления build_fix_loop."""

from __future__ import annotations

from pipeline.build_fix_loop import BuildFixLoop, CompilerError, parse_compiler_errors

LOG = """\
  Determining projects to restore...
  Api -> /src/bin/Debug/net10.0/Api.dll
Program.cs(14,25): error CS0246: The type or namespace name 'Foo' could not be found
1 Warning(s)
1 Error(s)
"""


def test_parse_compiler_errors_extracts_errors_only() -> None:
    errors = parse_compiler_errors(LOG)

    assert len(errors) == 1
    assert errors[0].path == "Program.cs"
    assert errors[0].line == 14
    assert errors[0].code == "CS0246"


def test_loop_success_on_first_build() -> None:
    calls: list[dict[str, str]] = []

    def build(files: dict[str, str]) -> tuple[bool, str]:
        calls.append(dict(files))
        return True, ""

    report = BuildFixLoop(build, fixer=None).run({"a.cs": "ok"})

    assert report.success
    assert report.attempts == 1
    assert report.fixed_files == []
    assert len(calls) == 1


def test_loop_fixes_single_file_and_passes() -> None:
    def build(files: dict[str, str]) -> tuple[bool, str]:
        if "error" in files["a.cs"]:
            return False, LOG
        return True, "Build succeeded"

    def fixer(path: str, content: str, error: CompilerError) -> tuple[str, int, int]:
        assert path == "a.cs"
        return content.replace("error", "fixed"), 10, 5

    report = BuildFixLoop(build, fixer).run({"a.cs": "error", "b.cs": "untouched"})

    assert report.success
    assert report.attempts == 2
    assert report.fixed_files == ["a.cs"]
    assert report.tokens_in == 10
    assert report.tokens_out == 5


def test_loop_stops_after_max_attempts() -> None:
    calls = 0

    def build(files: dict[str, str]) -> tuple[bool, str]:
        nonlocal calls
        calls += 1
        return False, LOG

    def fixer(path: str, content: str, error: CompilerError) -> tuple[str, int, int]:
        return content, 0, 0

    report = BuildFixLoop(build, fixer, max_attempts=3).run({"Program.cs": "broken"})

    assert not report.success
    assert report.attempts == 3
    assert calls == 4
    assert report.remaining_errors and report.remaining_errors[0].code == "CS0246"


def test_loop_accumulates_tokens_across_attempts() -> None:
    logs = iter(
        [
            LOG,
            "Other.cs(3,1): error CS1002: ; expected",
            "Build succeeded. 0 Error(s)",
        ]
    )

    def build(files: dict[str, str]) -> tuple[bool, str]:
        return "error" not in files, next(logs)

    def fixer(path: str, content: str, error: CompilerError) -> tuple[str, int, int]:
        return content + "// fixed", 7, 3

    report = BuildFixLoop(build, fixer).run({"Program.cs": "x", "Other.cs": "y"})

    assert report.success
    assert report.attempts == 3
    assert report.tokens_in == 14
    assert report.tokens_out == 6
    assert sorted(report.fixed_files) == ["Other.cs", "Program.cs"]

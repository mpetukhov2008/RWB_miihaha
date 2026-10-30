"""Детерминированная генерация SQL-миграций из data-model.json.

Строит миграции PostgreSQL по модели данных без LLM: таблицы, первичные
ключи, NOT NULL, индексы. Результат кладётся агентом 05 в
``generated/<case>/backend/db/migrations/``.
"""

from __future__ import annotations

import hashlib
from typing import Any

_PG_TYPE = {
    "string": "text",
    "uuid": "uuid",
    "integer": "bigint",
    "number": "numeric(18,2)",
    "boolean": "boolean",
    "datetime": "timestamptz",
    "geometry": "geometry",
}

_STRING_DEFAULTS = {"text"}

_ID_PG = "uuid PRIMARY KEY DEFAULT gen_random_uuid()"


def _snake(name: str) -> str:
    return "".join("_" + c.lower() if c.isupper() else c for c in name).lstrip("_")


def _pg_type(field: dict[str, Any]) -> str:
    return _PG_TYPE.get(str(field.get("type", "string")).lower(), "text")


def build_migrations(data_model: dict[str, Any]) -> dict[str, str]:
    statements: list[str] = []

    for ent in data_model.get("entities") or []:
        table = _snake(ent.get("name", "Entity"))
        statements.extend(_create_table(table, ent))
        statements.extend(_create_indexes(table, ent))

    if not statements:
        return {}

    body = "\n".join(statements)
    checksum = hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]
    header = (
        "-- Миграция сгенерирована пайплайном из data-model.json.\n"
        f"-- Контрольная сумма схемы: {checksum}\n"
        "-- Не редактировать вручную: правки вносить в data-model.json.\n"
    )
    sql = header + body + "\n"
    return {"db/migrations/001_init.sql": sql}


def _create_table(table: str, ent: dict[str, Any]) -> list[str]:
    columns: list[str] = []
    for f in ent.get("fields") or []:
        name = _snake(f.get("name", "field"))
        if name == "id":
            columns.append(f"    id {_ID_PG}")
            continue
        pg = _pg_type(f)
        not_null = " NOT NULL" if f.get("required") else ""
        default = " DEFAULT ''" if pg in _STRING_DEFAULTS and not f.get("required") else ""
        columns.append(f"    {name} {pg}{not_null}{default}")
    if not columns:
        columns = [f"    id {_ID_PG}"]

    lines = [f"CREATE TABLE IF NOT EXISTS {table} (", ",\n".join(columns), ");"]
    return ["\n".join(lines)]


def _create_indexes(table: str, ent: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for raw in ent.get("indexes") or []:
        spec = str(raw).strip()
        unique = spec.startswith("unique:")
        cols_spec = spec[len("unique:"):] if unique else spec
        cols = ", ".join(_snake(c.strip()) for c in cols_spec.split(",") if c.strip())
        if not cols:
            continue
        unique_sql = "UNIQUE " if unique else ""
        index_name = f"{table}_{'_'.join(cols.split(', '))}_idx"
        result.append(
            f"CREATE {unique_sql}INDEX IF NOT EXISTS {index_name} ON {table} ({cols});"
        )
    return result

"""Тесты детерминированного генератора SQL-миграций."""

from __future__ import annotations

from pipeline.generators.migrations import build_migrations

DATA_MODEL = {
    "entities": [
        {
            "name": "Session",
            "fields": [
                {"name": "id", "type": "uuid", "required": True},
                {"name": "userId", "type": "uuid", "required": True},
                {"name": "status", "type": "string", "required": True},
                {"name": "amount", "type": "number"},
                {"name": "startedAt", "type": "datetime", "required": True},
                {"name": "note", "type": "string"},
            ],
            "indexes": ["userId", "unique:status"],
        }
    ]
}


def test_generates_table_and_id_pk() -> None:
    files = build_migrations(DATA_MODEL)

    sql = files["db/migrations/001_init.sql"]
    assert "CREATE TABLE IF NOT EXISTS session (" in sql
    assert "id uuid PRIMARY KEY DEFAULT gen_random_uuid()" in sql


def test_field_types_mapped_to_postgres() -> None:
    sql = build_migrations(DATA_MODEL)["db/migrations/001_init.sql"]

    assert "user_id uuid NOT NULL" in sql
    assert "amount numeric(18,2)" in sql
    assert "started_at timestamptz NOT NULL" in sql
    assert "note text DEFAULT ''" in sql


def test_indexes_plain_and_unique() -> None:
    sql = build_migrations(DATA_MODEL)["db/migrations/001_init.sql"]

    assert "CREATE INDEX IF NOT EXISTS session_user_id_idx ON session (user_id);" in sql
    assert "CREATE UNIQUE INDEX IF NOT EXISTS session_status_idx ON session (status);" in sql


def test_empty_model_produces_no_files() -> None:
    assert build_migrations({}) == {}


def test_generation_is_deterministic() -> None:
    first = build_migrations(DATA_MODEL)
    second = build_migrations(DATA_MODEL)

    assert first == second

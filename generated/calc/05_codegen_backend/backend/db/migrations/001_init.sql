-- Миграция сгенерирована пайплайном из data-model.json.
-- Контрольная сумма схемы: aa819e31
-- Не редактировать вручную: правки вносить в data-model.json.
CREATE TABLE IF NOT EXISTS calculation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    first_number numeric(18,2) NOT NULL,
    second_number numeric(18,2) NOT NULL,
    result numeric(18,2) NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS calculation_id_idx ON calculation (id);

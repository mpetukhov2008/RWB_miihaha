-- Миграция сгенерирована пайплайном из data-model.json.
-- Контрольная сумма схемы: 81f4fe0f
-- Не редактировать вручную: правки вносить в data-model.json.
CREATE TABLE IF NOT EXISTS parking_zone (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    tariff_per_hour numeric(18,2) NOT NULL
);
CREATE INDEX IF NOT EXISTS parking_zone_name_idx ON parking_zone (name);
CREATE TABLE IF NOT EXISTS session (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id text NOT NULL,
    zone_id text NOT NULL,
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    status text NOT NULL
);
CREATE INDEX IF NOT EXISTS session_user_id_idx ON session (user_id);
CREATE INDEX IF NOT EXISTS session_status_idx ON session (status);
CREATE TABLE IF NOT EXISTS payment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id text NOT NULL,
    amount numeric(18,2) NOT NULL,
    status text NOT NULL
);
CREATE INDEX IF NOT EXISTS payment_session_id_idx ON payment (session_id);

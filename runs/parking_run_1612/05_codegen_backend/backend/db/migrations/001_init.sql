-- Миграция сгенерирована пайплайном из data-model.json.
-- Контрольная сумма схемы: 3865ba34
-- Не редактировать вручную: правки вносить в data-model.json.
CREATE TABLE IF NOT EXISTS user (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text NOT NULL,
    role text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS user_idx_user_email_idx ON user (idx_user_email);
CREATE INDEX IF NOT EXISTS user_idx_user_role_idx ON user (idx_user_role);
CREATE TABLE IF NOT EXISTS parking_zone (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    polygon text NOT NULL,
    rate_per_hour numeric(18,2) NOT NULL,
    currency text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz
);
CREATE INDEX IF NOT EXISTS parking_zone_idx_zone_name_idx ON parking_zone (idx_zone_name);
CREATE INDEX IF NOT EXISTS parking_zone_idx_zone_is_active_idx ON parking_zone (idx_zone_is_active);
CREATE TABLE IF NOT EXISTS parking_session (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id text NOT NULL,
    zone_id text NOT NULL,
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    duration_seconds bigint,
    rate_per_hour numeric(18,2) NOT NULL,
    amount numeric(18,2),
    status text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS parking_session_idx_session_user_id_idx ON parking_session (idx_session_user_id);
CREATE INDEX IF NOT EXISTS parking_session_idx_session_zone_id_idx ON parking_session (idx_session_zone_id);
CREATE INDEX IF NOT EXISTS parking_session_idx_session_status_idx ON parking_session (idx_session_status);
CREATE INDEX IF NOT EXISTS parking_session_idx_session_started_at_idx ON parking_session (idx_session_started_at);
CREATE TABLE IF NOT EXISTS payment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id text NOT NULL,
    amount numeric(18,2) NOT NULL,
    status text NOT NULL,
    created_at timestamptz NOT NULL,
    paid_at timestamptz
);
CREATE INDEX IF NOT EXISTS payment_idx_payment_session_id_idx ON payment (idx_payment_session_id);
CREATE INDEX IF NOT EXISTS payment_idx_payment_status_idx ON payment (idx_payment_status);
CREATE TABLE IF NOT EXISTS notification (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id text NOT NULL,
    session_id text NOT NULL,
    type text NOT NULL,
    message text NOT NULL,
    sent_at timestamptz NOT NULL,
    read_at timestamptz
);
CREATE INDEX IF NOT EXISTS notification_idx_notification_user_id_idx ON notification (idx_notification_user_id);
CREATE INDEX IF NOT EXISTS notification_idx_notification_session_id_idx ON notification (idx_notification_session_id);
CREATE INDEX IF NOT EXISTS notification_idx_notification_read_at_idx ON notification (idx_notification_read_at);

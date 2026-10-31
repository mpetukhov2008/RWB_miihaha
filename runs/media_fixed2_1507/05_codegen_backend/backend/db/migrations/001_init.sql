-- Миграция сгенерирована пайплайном из data-model.json.
-- Контрольная сумма схемы: dfffa707
-- Не редактировать вручную: правки вносить в data-model.json.
CREATE TABLE IF NOT EXISTS application (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    type text NOT NULL,
    status text NOT NULL,
    reference_file_id text NOT NULL,
    source_file_id text NOT NULL,
    result_file_id text DEFAULT '',
    similarity_score numeric(18,2),
    verification_status text DEFAULT '',
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS application_idx_application_status_idx ON application (idx_application_status);
CREATE INDEX IF NOT EXISTS application_idx_application_type_idx ON application (idx_application_type);
CREATE INDEX IF NOT EXISTS application_idx_application_created_at_idx ON application (idx_application_created_at);
CREATE TABLE IF NOT EXISTS media_file (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    s3_key text NOT NULL,
    file_type text NOT NULL,
    file_role text NOT NULL,
    size_bytes bigint NOT NULL,
    duration_seconds numeric(18,2),
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS media_file_idx_media_file_s3_key_idx ON media_file (idx_media_file_s3_key);
CREATE INDEX IF NOT EXISTS media_file_idx_media_file_role_idx ON media_file (idx_media_file_role);
CREATE TABLE IF NOT EXISTS video_segment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    start_time numeric(18,2) NOT NULL,
    end_time numeric(18,2) NOT NULL,
    confidence numeric(18,2) NOT NULL,
    result_file_id text DEFAULT '',
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS video_segment_idx_video_segment_application_id_idx ON video_segment (idx_video_segment_application_id);
CREATE TABLE IF NOT EXISTS processing_job (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    job_type text NOT NULL,
    status text NOT NULL,
    started_at timestamptz,
    completed_at timestamptz,
    error_message text DEFAULT ''
);
CREATE INDEX IF NOT EXISTS processing_job_idx_processing_job_application_id_idx ON processing_job (idx_processing_job_application_id);
CREATE INDEX IF NOT EXISTS processing_job_idx_processing_job_status_idx ON processing_job (idx_processing_job_status);

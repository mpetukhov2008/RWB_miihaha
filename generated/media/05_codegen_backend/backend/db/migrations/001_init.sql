-- Миграция сгенерирована пайплайном из data-model.json.
-- Контрольная сумма схемы: 658554b4
-- Не редактировать вручную: правки вносить в data-model.json.
CREATE TABLE IF NOT EXISTS application (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    type text NOT NULL,
    status text NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz
);
CREATE INDEX IF NOT EXISTS application_idx_application_status_idx ON application (idx_application_status);
CREATE INDEX IF NOT EXISTS application_idx_application_created_at_idx ON application (idx_application_created_at);
CREATE TABLE IF NOT EXISTS reference_template (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    s3_key text NOT NULL,
    format text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS reference_template_idx_reference_template_s3_key_idx ON reference_template (idx_reference_template_s3_key);
CREATE TABLE IF NOT EXISTS media_file (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    s3_key text NOT NULL,
    file_type text NOT NULL,
    duration_seconds numeric(18,2),
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS media_file_idx_media_file_application_id_idx ON media_file (idx_media_file_application_id);
CREATE INDEX IF NOT EXISTS media_file_idx_media_file_s3_key_idx ON media_file (idx_media_file_s3_key);
CREATE TABLE IF NOT EXISTS photo_analysis_result (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    similarity_score numeric(18,2) NOT NULL,
    status text NOT NULL,
    quality_metrics text DEFAULT '',
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS photo_analysis_result_idx_photo_analysis_application_id_idx ON photo_analysis_result (idx_photo_analysis_application_id);
CREATE TABLE IF NOT EXISTS video_analysis_result (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    segments text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS video_analysis_result_idx_video_analysis_application_id_idx ON video_analysis_result (idx_video_analysis_application_id);
CREATE TABLE IF NOT EXISTS video_segment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id text NOT NULL,
    start_time numeric(18,2) NOT NULL,
    end_time numeric(18,2) NOT NULL,
    confidence numeric(18,2)
);
CREATE INDEX IF NOT EXISTS video_segment_idx_video_segment_analysis_id_idx ON video_segment (idx_video_segment_analysis_id);
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

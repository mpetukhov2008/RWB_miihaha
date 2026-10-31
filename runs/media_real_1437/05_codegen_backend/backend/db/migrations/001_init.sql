-- Миграция сгенерирована пайплайном из data-model.json.
-- Контрольная сумма схемы: 29c927a9
-- Не редактировать вручную: правки вносить в data-model.json.
CREATE TABLE IF NOT EXISTS application (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    type text NOT NULL,
    status text NOT NULL,
    reference_file_id text NOT NULL,
    source_file_id text NOT NULL,
    result_file_id text DEFAULT '',
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS application_idx_application_status_idx ON application (idx_application_status);
CREATE INDEX IF NOT EXISTS application_idx_application_type_idx ON application (idx_application_type);
CREATE INDEX IF NOT EXISTS application_idx_application_created_at_idx ON application (idx_application_created_at);
CREATE TABLE IF NOT EXISTS reference_file (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    s3_key text NOT NULL,
    mime_type text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS reference_file_idx_reference_file_s3_key_idx ON reference_file (idx_reference_file_s3_key);
CREATE TABLE IF NOT EXISTS media_file (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    s3_key text NOT NULL,
    mime_type text NOT NULL,
    size_bytes bigint NOT NULL,
    duration_seconds numeric(18,2),
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS media_file_idx_media_file_s3_key_idx ON media_file (idx_media_file_s3_key);
CREATE INDEX IF NOT EXISTS media_file_idx_media_file_mime_type_idx ON media_file (idx_media_file_mime_type);
CREATE TABLE IF NOT EXISTS photo_analysis_result (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    similarity_score numeric(18,2) NOT NULL,
    quality_status text NOT NULL,
    match_status text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS photo_analysis_result_idx_photo_analysis_application_id_idx ON photo_analysis_result (idx_photo_analysis_application_id);
CREATE INDEX IF NOT EXISTS photo_analysis_result_idx_photo_analysis_match_status_idx ON photo_analysis_result (idx_photo_analysis_match_status);
CREATE TABLE IF NOT EXISTS video_analysis_result (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id text NOT NULL,
    segments text NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS video_analysis_result_idx_video_analysis_application_id_idx ON video_analysis_result (idx_video_analysis_application_id);
CREATE TABLE IF NOT EXISTS video_segment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    video_analysis_id text NOT NULL,
    start_time numeric(18,2) NOT NULL,
    end_time numeric(18,2) NOT NULL,
    result_file_id text DEFAULT ''
);
CREATE INDEX IF NOT EXISTS video_segment_idx_video_segment_analysis_id_idx ON video_segment (idx_video_segment_analysis_id);

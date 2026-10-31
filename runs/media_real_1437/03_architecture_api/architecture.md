# Архитектура

## Модель данных
### Application
Заявка на проверку рекламной конструкции (фото или видео).
- `id`: `string` (required) — Уникальный идентификатор заявки (UUID).
- `type`: `string` (required) — Тип заявки: photo, video.
- `status`: `string` (required) — Статус обработки: pending, processing, completed, failed.
- `reference_file_id`: `string` (required) — Идентификатор эталонного макета (ReferenceFile).
- `source_file_id`: `string` (required) — Идентификатор исходного медиафайла (MediaFile).
- `result_file_id`: `string` — Идентификатор итогового медиафайла (MediaFile), если применимо.
- `created_at`: `datetime` (required) — Дата и время создания заявки.
- `updated_at`: `datetime` (required) — Дата и времени последнего обновления.

### ReferenceFile
Эталонный статический макет (JPEG/PNG), используемый для сверки.
- `id`: `string` (required) — Уникальный идентификатор эталонного макета (UUID).
- `s3_key`: `string` (required) — Ключ файла в S3.
- `mime_type`: `string` (required) — Тип MIME (image/jpeg, image/png).
- `created_at`: `datetime` (required) — Дата и время загрузки.

### MediaFile
Исходный или итоговый медиафайл (фото или видео).
- `id`: `string` (required) — Уникальный идентификатор медиафайла (UUID).
- `s3_key`: `string` (required) — Ключ файла в S3.
- `mime_type`: `string` (required) — Тип MIME (image/jpeg, image/png, video/mp4).
- `size_bytes`: `integer` (required) — Размер файла в байтах.
- `duration_seconds`: `number` — Длительность видео в секундах (для видеофайлов).
- `created_at`: `datetime` (required) — Дата и время загрузки.

### PhotoAnalysisResult
Результат анализа фотографии: качество и соответствие макету.
- `id`: `string` (required) — Уникальный идентификатор результата (UUID).
- `application_id`: `string` (required) — Идентификатор заявки (Application).
- `similarity_score`: `number` (required) — Процент схожести с эталонным макетом (0-100).
- `quality_status`: `string` (required) — Статус качества: low_quality, acceptable.
- `match_status`: `string` (required) — Статус соответствия: matches, does_not_match, low_quality.
- `created_at`: `datetime` (required) — Дата и время завершения анализа.

### VideoAnalysisResult
Результат анализа видеопотока: временные метки обнаруженных роликов.
- `id`: `string` (required) — Уникальный идентификатор результата (UUID).
- `application_id`: `string` (required) — Идентификатор заявки (Application).
- `segments`: `array` (required) — Массив обнаруженных сегментов (start_time, end_time).
- `created_at`: `datetime` (required) — Дата и время завершения анализа.

### VideoSegment
Обнаруженный сегмент рекламного ролика в исходном видео.
- `id`: `string` (required) — Уникальный идентификатор сегмента (UUID).
- `video_analysis_id`: `string` (required) — Идентификатор результата видеоанализа (VideoAnalysisResult).
- `start_time`: `number` (required) — Начальная временная метка в секундах.
- `end_time`: `number` (required) — Конечная временная метка в секундах.
- `result_file_id`: `string` — Идентификатор вырезанного файла (MediaFile), если нарезка выполнена.

## События
- **ApplicationCreated** v1: Создана новая заявка на обработку медиафайла.
- **ApplicationProcessingStarted** v1: Начата обработка заявки.
- **PhotoAnalysisCompleted** v1: Завершен анализ фотографии.
- **VideoAnalysisCompleted** v1: Завершен анализ видеопотока, обнаружены временные метки.
- **VideoSegmentCut** v1: Вырезан целевой 15-секундный фрагмент видео.
- **ApplicationCompleted** v1: Заявка успешно обработана, итоговый файл сохранен в S3.
- **ApplicationFailed** v1: Обработка заявки завершилась ошибкой.

## API
- `POST /applications` — createApplication (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `GET /applications/{id}` — getApplication (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `GET /applications/{id}/photo-result` — getPhotoAnalysisResult (auth)
  - требования: FR-001
- `GET /applications/{id}/video-result` — getVideoAnalysisResult (auth)
  - требования: FR-002, FR-003
- `POST /applications/{id}/process` — triggerProcessing (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /files/upload-url` — getUploadUrl (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /files/{id}/confirm-upload` — confirmFileUpload (auth)
  - требования: FR-001, FR-002, FR-003, FR-004

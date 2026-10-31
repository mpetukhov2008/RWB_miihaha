# Архитектура

## Модель данных
### Application
Заявка на проверку рекламной конструкции (фото или видео).
- `id`: `string` (required) — Уникальный идентификатор заявки (UUID).
- `type`: `string` (required) — Тип заявки: photo | video.
- `status`: `string` (required) — Статус обработки: pending | processing | completed | failed.
- `reference_file_id`: `string` (required) — Идентификатор эталонного макета (JPEG/PNG).
- `source_file_id`: `string` (required) — Идентификатор исходного медиафайла (фото или видео).
- `result_file_id`: `string` — Идентификатор итогового файла в S3 (при успешной обработке).
- `similarity_score`: `number` — Процент схожести с макетом (для фото).
- `verification_status`: `string` — Результат верификации: matches | does_not_match | low_quality.
- `created_at`: `datetime` (required) — Время создания заявки.
- `updated_at`: `datetime` (required) — Время последнего обновления.

### MediaFile
Медиафайл (исходный, эталонный или итоговый), хранящийся в S3.
- `id`: `string` (required) — Уникальный идентификатор файла (UUID).
- `s3_key`: `string` (required) — Ключ объекта в S3.
- `file_type`: `string` (required) — Тип файла: jpeg | png | mp4.
- `file_role`: `string` (required) — Роль файла: source | reference | result.
- `size_bytes`: `integer` (required) — Размер файла в байтах.
- `duration_seconds`: `number` — Длительность видео в секундах (для видеофайлов).
- `created_at`: `datetime` (required) — Время загрузки файла.

### VideoSegment
Обнаруженный фрагмент рекламного ролика в исходном видео.
- `id`: `string` (required) — Уникальный идентификатор сегмента (UUID).
- `application_id`: `string` (required) — Идентификатор заявки.
- `start_time`: `number` (required) — Начальная временная метка (секунды).
- `end_time`: `number` (required) — Конечная временная метка (секунды).
- `confidence`: `number` (required) — Уверенность детекции (0-1).
- `result_file_id`: `string` — Идентификатор вырезанного файла в S3.
- `created_at`: `datetime` (required) — Время обнаружения сегмента.

### ProcessingJob
Задача обработки медиафайла (фото или видео).
- `id`: `string` (required) — Уникальный идентификатор задачи (UUID).
- `application_id`: `string` (required) — Идентификатор заявки.
- `job_type`: `string` (required) — Тип задачи: photo_verification | video_detection | video_cutting.
- `status`: `string` (required) — Статус задачи: queued | running | completed | failed.
- `started_at`: `datetime` — Время начала обработки.
- `completed_at`: `datetime` — Время завершения обработки.
- `error_message`: `string` — Сообщение об ошибке (при неудаче).

## События
- **ApplicationCreated** v1: Создана новая заявка на обработку.
- **PhotoVerificationCompleted** v1: Завершена верификация фотографии.
- **VideoDetectionCompleted** v1: Завершена детекция рекламных роликов в видео.
- **VideoCuttingCompleted** v1: Завершена нарезка видеофайлов.
- **ApplicationCompleted** v1: Заявка полностью обработана, результаты сохранены в S3.
- **ApplicationFailed** v1: Обработка заявки завершилась ошибкой.

## API
- `POST /applications` — createApplication (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `GET /applications/{id}` — getApplication (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /files/upload-url` — getUploadUrl (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /files/{id}/confirm` — confirmFileUpload (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /applications/{id}/process` — triggerProcessing (auth)
  - требования: FR-001, FR-002, FR-003
- `GET /applications/{id}/segments` — getVideoSegments (auth)
  - требования: FR-002, FR-003
- `GET /files/{id}/download-url` — getDownloadUrl (auth)
  - требования: FR-004

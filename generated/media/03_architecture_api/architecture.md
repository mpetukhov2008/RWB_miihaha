# Архитектура

## Модель данных
### Application
Заявка на проверку рекламной конструкции (фото или видео).
- `id`: `string` (required) — Уникальный идентификатор заявки (UUID).
- `type`: `string` (required) — Тип заявки: photo, video.
- `status`: `string` (required) — Статус обработки: pending, processing, completed, failed.
- `created_at`: `datetime` (required) — Дата и время создания заявки.
- `updated_at`: `datetime` — Дата и времени последнего обновления.

### ReferenceTemplate
Эталонный фотомакет (JPEG/PNG) для сверки.
- `id`: `string` (required) — Уникальный идентификатор шаблона (UUID).
- `s3_key`: `string` (required) — Ключ файла в S3.
- `format`: `string` (required) — Формат файла: JPEG, PNG.
- `created_at`: `datetime` (required) — Дата и время создания.

### MediaFile
Исходный или итоговый медиафайл (фото или видео).
- `id`: `string` (required) — Уникальный идентификатор файла (UUID).
- `application_id`: `string` (required) — Идентификатор связанной заявки.
- `s3_key`: `string` (required) — Ключ файла в S3.
- `file_type`: `string` (required) — Тип файла: source_photo, source_video, result_photo, result_video.
- `duration_seconds`: `number` — Длительность видео в секундах (для видеофайлов).
- `created_at`: `datetime` (required) — Дата и время загрузки.

### PhotoAnalysisResult
Результат анализа фотографии.
- `id`: `string` (required) — Уникальный идентификатор результата (UUID).
- `application_id`: `string` (required) — Идентификатор связанной заявки.
- `similarity_score`: `number` (required) — Процент схожести с эталоном (0-100).
- `status`: `string` (required) — Статус: matches_template, does_not_match, low_quality.
- `quality_metrics`: `object` — Метрики качества: focus, lighting, glare.
- `created_at`: `datetime` (required) — Дата и время анализа.

### VideoAnalysisResult
Результат анализа видеопотока.
- `id`: `string` (required) — Уникальный идентификатор результата (UUID).
- `application_id`: `string` (required) — Идентификатор связанной заявки.
- `segments`: `array` (required) — Массив найденных сегментов с временными метками.
- `created_at`: `datetime` (required) — Дата и времени анализа.

### VideoSegment
Найденный сегмент рекламного ролика в видео.
- `id`: `string` (required) — Уникальный идентификатор сегмента (UUID).
- `analysis_id`: `string` (required) — Идентификатор связанного анализа.
- `start_time`: `number` (required) — Начальная временная метка (секунды).
- `end_time`: `number` (required) — Конечная временная метка (секунды).
- `confidence`: `number` — Уверенность определения (0-1).

### ProcessingJob
Задача обработки медиафайла.
- `id`: `string` (required) — Уникальный идентификатор задачи (UUID).
- `application_id`: `string` (required) — Идентификатор связанной заявки.
- `job_type`: `string` (required) — Тип задачи: photo_analysis, video_analysis, video_cutting.
- `status`: `string` (required) — Статус: queued, running, completed, failed.
- `started_at`: `datetime` — Дата и время начала обработки.
- `completed_at`: `datetime` — Дата и время завершения обработки.
- `error_message`: `string` — Сообщение об ошибке (при неудаче).

## События
- **ApplicationCreated** v1: Создана новая заявка на обработку.
- **PhotoAnalysisCompleted** v1: Завершен анализ фотографии.
- **VideoAnalysisCompleted** v1: Завершен анализ видеопотока.
- **VideoCuttingCompleted** v1: Завершена нарезка видео.
- **ProcessingFailed** v1: Ошибка при обработке.

## API
- `POST /applications` — createApplication (auth)
  - требования: FR-001, FR-002
- `GET /applications/{applicationId}` — getApplication (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /applications/{applicationId}/process` — triggerProcessing (auth)
  - требования: FR-001, FR-002, FR-003
- `GET /applications/{applicationId}/results` — getApplicationResults (auth)
  - требования: FR-001, FR-002, FR-003, FR-004
- `POST /reference-templates` — uploadReferenceTemplate (auth)
  - требования: FR-001, FR-002
- `GET /reference-templates/{templateId}` — getReferenceTemplate (auth)
  - требования: FR-001, FR-002
- `POST /webhooks/status` — receiveStatusWebhook (auth)
  - требования: FR-004

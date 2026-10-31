# Архитектура

## Модель данных
### User
Пользователь системы (водитель или администратор).
- `id`: `string` (required) — Уникальный идентификатор пользователя (UUID).
- `email`: `string` (required) — Электронная почта для аутентификации.
- `role`: `string` (required) — Роль: driver или admin.
- `created_at`: `datetime` (required) — Дата и время создания записи.

### ParkingZone
Платная парковочная зона с тарифом.
- `id`: `string` (required) — Уникальный идентификатор зоны (UUID).
- `name`: `string` (required) — Название зоны.
- `polygon`: `string` (required) — Географический полигон зоны (GeoJSON или WKT).
- `rate_per_hour`: `number` (required) — Тариф за час парковки.
- `is_active`: `boolean` (required) — Флаг активности зоны.
- `created_at`: `datetime` (required) — Дата и время создания.
- `updated_at`: `datetime` — Дата и время последнего обновления.

### ParkingSession
Парковочная сессия водителя.
- `id`: `string` (required) — Уникальный идентификатор сессии (UUID).
- `user_id`: `string` (required) — Идентификатор водителя.
- `zone_id`: `string` (required) — Идентификатор зоны.
- `started_at`: `datetime` (required) — Время начала сессии.
- `ended_at`: `datetime` — Время окончания сессии (null, если активна).
- `duration_minutes`: `integer` — Длительность сессии в минутах.
- `cost`: `number` — Итоговая стоимость сессии.
- `status`: `string` (required) — Статус: active, completed, overdue.
- `created_at`: `datetime` (required) — Дата и время создания записи.

### Payment
Mock-платёж по сессии.
- `id`: `string` (required) — Уникальный идентификатор платежа (UUID).
- `session_id`: `string` (required) — Идентификатор сессии.
- `amount`: `number` (required) — Сумма платежа.
- `status`: `string` (required) — Статус: pending, paid, failed.
- `created_at`: `datetime` (required) — Дата и время создания.
- `updated_at`: `datetime` — Дата и время обновления статуса.

### Notification
Уведомление для водителя.
- `id`: `string` (required) — Уникальный идентификатор уведомления (UUID).
- `user_id`: `string` (required) — Идентификатор получателя.
- `session_id`: `string` (required) — Идентификатор связанной сессии.
- `type`: `string` (required) — Тип: session_started, ending_soon, overdue.
- `message`: `string` (required) — Текст уведомления.
- `sent_at`: `datetime` — Время отправки.
- `created_at`: `datetime` (required) — Дата и время создания.

## События
- **SessionStarted** v1: Событие начала парковочной сессии.
- **SessionEndingSoon** v1: Событие о скором окончании оплаченного времени (за 5 минут).
- **SessionOverdue** v1: Событие о превышении оплаченного времени.
- **SessionCompleted** v1: Событие завершения парковочной сессии.
- **PaymentSettled** v1: Событие подтверждения mock-оплаты.
- **ZoneUpdated** v1: Событие изменения параметров зоны.

## API
- `POST /auth/login` — login
  - требования: NFR-002
- `GET /zones/nearby` — getNearbyZone (auth)
  - требования: FR-001
- `POST /sessions` — startSession (auth)
  - требования: FR-002, FR-005
- `GET /sessions/active` — getActiveSession (auth)
  - требования: FR-002
- `POST /sessions/{session_id}/end` — endSession (auth)
  - требования: FR-002, FR-005
- `GET /sessions/history` — getSessionHistory (auth)
  - требования: FR-004
- `GET /notifications` — getNotifications (auth)
  - требования: FR-003
- `GET /admin/zones` — adminListZones (auth)
  - требования: FR-006
- `POST /admin/zones` — adminCreateZone (auth)
  - требования: FR-006
- `PUT /admin/zones/{zone_id}` — adminUpdateZone (auth)
  - требования: FR-006
- `GET /admin/sessions` — adminListSessions (auth)
  - требования: FR-006
- `GET /admin/sessions/history` — adminSessionHistory (auth)
  - требования: FR-006

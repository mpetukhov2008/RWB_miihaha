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
- `currency`: `string` (required) — Валюта тарифа (например, RUB).
- `is_active`: `boolean` (required) — Флаг активности зоны.
- `created_at`: `datetime` (required) — Дата и время создания.
- `updated_at`: `datetime` — Дата и время последнего обновления.

### ParkingSession
Парковочная сессия водителя в зоне.
- `id`: `string` (required) — Уникальный идентификатор сессии (UUID).
- `user_id`: `string` (required) — Идентификатор водителя.
- `zone_id`: `string` (required) — Идентификатор зоны.
- `started_at`: `datetime` (required) — Время начала сессии.
- `ended_at`: `datetime` — Время окончания сессии (null, если активна).
- `duration_seconds`: `integer` — Длительность сессии в секундах (заполняется при завершении).
- `rate_per_hour`: `number` (required) — Тариф, зафиксированный на момент начала.
- `amount`: `number` — Итоговая стоимость (заполняется при завершении).
- `status`: `string` (required) — Статус: active, completed, overdue.
- `created_at`: `datetime` (required) — Дата и время создания записи.

### Payment
Mock-платёж, связанный с парковочной сессией.
- `id`: `string` (required) — Уникальный идентификатор платежа (UUID).
- `session_id`: `string` (required) — Идентификатор сессии.
- `amount`: `number` (required) — Сумма платежа.
- `status`: `string` (required) — Статус: pending, paid, failed.
- `created_at`: `datetime` (required) — Дата и время создания.
- `paid_at`: `datetime` — Дата и время оплаты.

### Notification
Уведомление, отправленное водителю.
- `id`: `string` (required) — Уникальный идентификатор уведомления (UUID).
- `user_id`: `string` (required) — Идентификатор получателя.
- `session_id`: `string` (required) — Идентификатор связанной сессии.
- `type`: `string` (required) — Тип: session_started, ending_soon, overdue.
- `message`: `string` (required) — Текст уведомления.
- `sent_at`: `datetime` (required) — Время отправки.
- `read_at`: `datetime` — Время прочтения (null, если не прочитано).

## События
- **SessionStarted** v1: Событие начала парковочной сессии.
- **SessionEndingSoon** v1: Событие о скором окончании оплаченного времени (за 5 минут).
- **SessionOverdue** v1: Событие о превышении оплаченного времени.
- **SessionCompleted** v1: Событие завершения парковочной сессии.
- **PaymentSettled** v1: Событие фиксации mock-оплаты по факту.
- **ZoneUpdated** v1: Событие изменения зоны или тарифа администратором.

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
- `GET /sessions` — listMySessions (auth)
  - требования: FR-004
- `GET /notifications` — listNotifications (auth)
  - требования: FR-003
- `POST /notifications/{notification_id}/read` — markNotificationRead (auth)
  - требования: FR-003
- `GET /admin/zones` — adminListZones (auth)
  - требования: FR-006, NFR-002
- `POST /admin/zones` — adminCreateZone (auth)
  - требования: FR-006, NFR-002
- `PUT /admin/zones/{zone_id}` — adminUpdateZone (auth)
  - требования: FR-006, NFR-002
- `GET /admin/sessions` — adminListSessions (auth)
  - требования: FR-006, NFR-002

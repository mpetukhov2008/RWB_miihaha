# Архитектура

## Модель данных
### ParkingZone
Платная зона
- `id`: `string` (required) — UUID
- `name`: `string` (required) — Название
- `tariffPerHour`: `number` (required) — Тариф

### Session
Парковочная сессия
- `id`: `string` (required) — UUID
- `userId`: `string` (required) — Водитель
- `zoneId`: `string` (required) — Зона
- `startedAt`: `datetime` (required) — Начало
- `endedAt`: `datetime` — Конец
- `status`: `string` (required) — active/completed

### Payment
Mock-платёж
- `id`: `string` (required) — UUID
- `sessionId`: `string` (required) — Сессия
- `amount`: `number` (required) — Сумма
- `status`: `string` (required) — pending/paid

## События
- **SessionStarted** v1: Сессия начата
- **SessionCompleted** v1: Сессия завершена

## API
- `GET /zones/{zoneId}` — getZone
  - требования: FR-001
- `POST /sessions` — startSession (auth)
  - требования: FR-001, FR-002, FR-005
- `POST /sessions/{sessionId}/complete` — completeSession (auth)
  - требования: FR-002, FR-005
- `GET /sessions` — listSessions (auth)
  - требования: FR-004
- `POST /admin/zones` — createZone (auth)
  - требования: FR-006, NFR-002

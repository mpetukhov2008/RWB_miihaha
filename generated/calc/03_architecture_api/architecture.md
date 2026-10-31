# Архитектура

## Модель данных
### Calculation
Сущность, представляющая операцию суммирования двух чисел
- `id`: `string` (required) — Уникальный идентификатор операции
- `first_number`: `number` (required) — Первое число для суммирования
- `second_number`: `number` (required) — Второе число для суммирования
- `result`: `number` (required) — Результат суммирования
- `created_at`: `datetime` (required) — Время создания операции

## События
- **CalculationCompleted** v1: Событие успешного завершения операции суммирования
- **CalculationFailed** v1: Событие ошибки при обработке операции суммирования

## API
- `POST /calculations` — createCalculation
  - требования: FR-001, FR-002, FR-003, NFR-001, NFR-002

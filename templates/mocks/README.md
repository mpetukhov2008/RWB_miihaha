# Mock-сервисы и адаптер провайдера

Чтобы пайплайн оставался универсальным и не зависел от внешних систем
(городской гео-сервис, реальная оплата), вводится интерфейс
`IParkingProvider` и mock-реализации.

## IParkingProvider

```csharp
public interface IParkingProvider
{
    IReadOnlyList<ParkingZone> LoadZones();
}
```

- `JsonParkingProvider` — читает зоны из JSON (например, `data/spb.json`);
- `InMemoryParkingProvider` — для тестов и демо.

## Mock-оплата

- `PaymentServiceMock` — имитирует платёж: `pending` → `paid`.
- В реальном проде заменяется на `IPaymentProvider` без изменения API.

## Зачем

- CI и демо работают без внешних систем (без сети).
- «Модель ничего не запускает»: эти классы — детерминированные mock'и,
  их вызывает Python-код пайплайна в тестах/демо.

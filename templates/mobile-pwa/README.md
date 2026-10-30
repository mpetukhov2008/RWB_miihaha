# Мобильный PWA-клиент

Каркас мобильного клиента (Angular 20.1.6 + Material 20 + service worker).
Копируется в `generated/<case>/frontend-mobile/` агентом 06 и дополняется
экранами из `ui-spec.json`.

## Состав

- Экран «локация» — ближайший объект к GPS-точке (запрос `GET /locations/nearest`);
- Экран «сессия» — статус активной сессии, обратный отсчёт, предупреждение за 10 минут;
- Экран «оплата» — переход по ссылке mock-провайдера (без реальной оплаты);
- PWA: `manifest.webmanifest`, service worker (`ngsw-config.json`, offline-кэш).

## Универсальность

В шаблоне нет терминологии конкретного кейса: «локация», «сессия», «оплата» —
настраиваются артефактами (`openapi.yaml`, `ui-spec.json`).

## Проверка

```bash
npm install
npm run build   # с service worker
npm start
```

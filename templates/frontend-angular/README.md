# Frontend-шаблон: Angular 20.1.6 + Angular Material

Каркас, который агент 06 наполняет экранами из `ui-spec.json` по правилам
`templates/ui-kit-rules.md`.

## Запуск

```bash
cd templates/frontend-angular
npm install --legacy-peer-deps
npm start        # dev
npm run build    # prod
```

## Структура (генерируется агентом 06)

- `src/app/screens/SCR_xxx/*.ts` — экраны из ui-spec.json;
- `src/app/components/*.ts` — переиспользуемые компоненты;
- `src/app/services/*.ts` — API-клиенты из openapi.yaml;
- `src/environments/environment.ts` — `{ apiUrl }`.

## PWA

`src/manifest.webmanifest` — заготовка PWA (start_url, standalone). Полный
service worker добавляется при необходимости (агент 06 / вручную).

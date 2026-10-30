# Правила UI Kit (Angular Material 20)

Эти правила обязательны для всех агентов-генераторов фронтенда (агент 06)
и для любых ручных правок UI.

## Выбор компонентов

- Используй **Angular Material 20.1.6** (тема `indigo-pink`), не самописные
  наборы кнопок/инпутов.
- Таблицы (списки) — `MatTable`, формы — `MatFormField` + `MatInput`,
  выбор — `MatSelect`, действия — `MatButton`, уведомления — `MatSnackBar`.
- Иконки — Material Icons (шрифт), не картинки.

## Состояния экрана (из ui-spec.json)

Каждый экран обязан отрабатывать состояния:
- `empty` — сообщение «Нет данных» + действие «Обновить»;
- `loading` — `MatProgressSpinner`;
- `error` — `MatSnackBar` или inline-блок с ошибкой;
- `forbidden` (если экран требует auth) — страница «Доступ запрещён»;
- `success` — подтверждение действия (snackbar).

## Сетка и отступы

- Контейнер: `max-width: 960px; margin: 0 auto; padding: 16px;`
- Отступы между карточками: `16px`.
- Заголовок экрана: `h1/h2` Material typography.

## API

- Вызовы API — через `HttpClient` + `provideHttpClient()`, base URL из
  `environment.apiUrl` (injection token).
- Ошибки API приводятся к `ProblemDetails` (единый формат из backend).

## Запрещено

- Самописная вёрстка вместо Material-компонентов.
- Жёсткие цвета вне темы Material.
- Прямые DOM-манипуляции (только Angular-привязки).

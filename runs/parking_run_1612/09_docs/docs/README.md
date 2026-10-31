# Парковочное приложение (MVP)

MVP-приложение для управления платной парковкой: водитель начинает/завершает сессию, получает уведомления, смотрит историю; администратор управляет зонами и тарифами.

## Требования

- Node.js 20+
- Docker и Docker Compose
- npm

## Установка (install)

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd parking-app

# 2. Установить зависимости
cd backend && npm install
cd ../mobile && npm install

# 3. Инициализировать БД (если используется локальная)
cd backend && npm run db:init
```

## Запуск (run)

### Вариант 1: Docker Compose (рекомендуется)

```bash
docker compose up -d
```

- Backend API: http://localhost:3000
- Mobile (Angular): http://localhost:4200
- Admin panel: http://localhost:4200/admin

### Вариант 2: Локальный запуск

```bash
# Backend
cd backend
npm run dev

# Mobile
cd mobile
npm start
```

## Тестирование (test)

```bash
# Unit-тесты backend
cd backend && npm test

# E2E-тесты
cd backend && npm run test:e2e

# Тесты mobile
cd mobile && npm test
```

## Структура проекта

```
parking-app/
├── backend/          # REST API (Node.js/Express)
├── mobile/           # Angular mobile app
├── docs/             # Документация
└── docker-compose.yml
```

## Документация

- [Руководство пользователя](docs/user-guide.md)
- [Известные ограничения](docs/known-limitations.md)
- [Инструкции по запуску](docs/run-instructions.md)
- [Гид для разработчика](docs/dev-guide.md)
- [Продуктовое описание](docs/product-description.md)

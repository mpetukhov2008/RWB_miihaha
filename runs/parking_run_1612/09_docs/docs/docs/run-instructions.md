# Инструкции по запуску

## Требования

- Docker 20.10+
- Docker Compose 2.0+
- 4 ГБ RAM минимум
- 10 ГБ свободного места на диске

## Запуск через Docker Compose

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd parking-app
```

### 2. Настроить переменные окружения

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

Пример `.env`:

```env
# Backend
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=parking
DB_USER=parking
DB_PASSWORD=parking_secret

# Mobile
API_URL=http://localhost:3000

# Auth
JWT_SECRET=change_this_secret
JWT_EXPIRES_IN=24h
```

### 3. Запустить контейнеры

```bash
docker compose up -d
```

### 4. Проверить статус

```bash
docker compose ps
```

Ожидаемый вывод:

```
NAME                STATUS
parking-backend     Up
parking-mobile      Up
parking-db          Up
```

### 5. Открыть приложение

- **Mobile app**: http://localhost:4200
- **Admin panel**: http://localhost:4200/admin
- **API docs**: http://localhost:3000/api/docs

## Остановка

```bash
docker compose down
```

## Очистка данных

```bash
docker compose down -v
```

> **Внимание**: команда удаляет все данные из БД.

## Логи

```bash
# Логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f backend
```

## Обновление

```bash
git pull
docker compose down
docker compose up -d
```

## Устранение неполадок

### Контейнер не запускается

```bash
# Проверить логи
docker compose logs backend

# Пересоздать контейнер
docker compose up -d --force-recreate backend
```

### БД не подключается

```bash
# Проверить статус БД
docker compose ps db

# Перезапустить БД
docker compose restart db
```

### Порт занят

Измените порт в `docker-compose.yml` или освободите занятый порт.

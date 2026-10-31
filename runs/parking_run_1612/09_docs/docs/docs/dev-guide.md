# Гид для разработчика

## Архитектура

### Обзор

Система состоит из трёх основных компонентов:

1. **Backend API** — REST API на Node.js/Express
2. **Mobile App** — Angular mobile application
3. **Database** — PostgreSQL

### Схема архитектуры

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Mobile App │────▶│  Backend API │────▶│  PostgreSQL │
│  (Angular)  │◀────│  (Node.js)   │◀────│             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│  Geolocation │     │  Push       │
│  Service     │     │  Notifications│
└─────────────┘     └─────────────┘
```

## Backend

### Технологии

- Node.js 20+
- Express
- PostgreSQL
- JWT для аутентификации

### Структура

```
backend/
├── src/
│   ├── config/          # Конфигурация
│   ├── controllers/     # Контроллеры
│   ├── models/          # Модели данных
│   ├── routes/          # Маршруты API
│   ├── services/        # Бизнес-логика
│   ├── middleware/      # Middleware (auth, error handling)
│   └── utils/           # Утилиты
├── tests/
│   ├── unit/            # Unit-тесты
│   └── e2e/             # E2E-тесты
├── package.json
└── Dockerfile
```

### API Endpoints

#### Auth

- `POST /api/auth/login` — логин
- `POST /api/auth/register` — регистрация

#### Zones

- `GET /api/zones` — список зон
- `GET /api/zones/:id` — информация о зоне
- `POST /api/zones` — создать зону (admin)
- `PUT /api/zones/:id` — редактировать зону (admin)
- `DELETE /api/zones/:id` — удалить зону (admin)

#### Sessions

- `POST /api/sessions` — начать сессию
- `GET /api/sessions/active` — активная сессия
- `POST /api/sessions/:id/complete` — завершить сессию
- `GET /api/sessions/history` — история сессий

#### Admin

- `GET /api/admin/sessions/active` — активные сессии (admin)
- `GET /api/admin/sessions/history` — история сессий (admin)

### Модели данных

#### Zone

```typescript
interface Zone {
  id: string;
  name: string;
  tariff: number; // стоимость в час
  polygon: [number, number][]; // координаты зоны
  createdAt: Date;
  updatedAt: Date;
}
```

#### Session

```typescript
interface Session {
  id: string;
  userId: string;
  zoneId: string;
  startTime: Date;
  endTime: Date | null;
  status: 'active' | 'completed' | 'overdue';
  cost: number;
  paymentId: string;
  createdAt: Date;
}
```

#### Payment

```typescript
interface Payment {
  id: string;
  sessionId: string;
  amount: number;
  status: 'pending' | 'paid' | 'failed';
  createdAt: Date;
  updatedAt: Date;
}
```

#### User

```typescript
interface User {
  id: string;
  email: string;
  passwordHash: string;
  role: 'driver' | 'admin';
  createdAt: Date;
}
```

## Mobile App

### Технологии

- Angular 20.1.6 (по умолчанию, см. Q-001)
- TypeScript
- RxJS

### Структура

```
mobile/
├── src/
│   ├── app/
│   │   ├── core/          # Сервисы, guards, interceptors
│   │   ├── features/
│   │   │   ├── auth/      # Логин/регистрация
│   │   │   ├── zone/      # Определение зоны
│   │   │   ├── session/   # Активная сессия
│   │   │   ├── history/   # История парковок
│   │   │   └── admin/     # Admin-панель
│   │   └── shared/        # Общие компоненты, pipes, directives
│   ├── assets/
│   └── environments/
├── package.json
└── angular.json
```

### Ключевые сервисы

#### GeolocationService

- Определение текущей позиции
- Проверка нахождения в платной зоне
- Обработка ошибок геолокации

#### SessionService

- Управление активной сессией
- Таймер сессии
- Расчёт стоимости

#### NotificationService

- Push-уведомления
- Таймеры для уведомлений

#### AuthService

- Аутентификация
- Управление токеном

## База данных

### Схема

```sql
-- Таблица пользователей
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'driver',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица зон
CREATE TABLE zones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  tariff DECIMAL(10, 2) NOT NULL,
  polygon JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица сессий
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  zone_id UUID REFERENCES zones(id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  cost DECIMAL(10, 2) DEFAULT 0,
  payment_id UUID,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица платежей
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(id),
  amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Тестирование

### Unit-тесты

```bash
cd backend && npm test
```

### E2E-тесты

```bash
cd backend && npm run test:e2e
```

### Тесты mobile

```bash
cd mobile && npm test
```

## CI/CD

### Pipeline

1. **Lint** — проверка стиля кода
2. **Unit tests** — unit-тесты
3. **Build** — сборка
4. **E2E tests** — E2E-тесты
5. **Docker build** — сборка Docker-образа
6. **Deploy** — деплой

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=parking
      - DB_USER=parking
      - DB_PASSWORD=parking_secret
    depends_on:
      - db

  mobile:
    build: ./mobile
    ports:
      - "4200:4200"
    environment:
      - API_URL=http://localhost:3000

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=parking
      - POSTGRES_USER=parking
      - POSTGRES_PASSWORD=parking_secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## Безопасность

- JWT-токены с истечением 24 часа
- Хеширование паролей (bcrypt)
- Role-based access control (RBAC)
- Валидация входных данных
- CORS-конфигурация

## Производительность

- Индексы на часто используемых полях
- Кэширование горячих данных
- Оптимизация SQL-запросов
- Цель: 95-й перцентиль < 300 мс (NFR-001)

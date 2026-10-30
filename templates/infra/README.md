# Инфраструктура (шаблон)

Содержимое этой папки копируется в `generated/<case>/infra/` и адаптируется
детерминированно под конкретный кейс (имя сервиса, порты, переменные).

Файлы:
- `docker-compose.yml` — PostGIS + API + frontend с healthcheck'ами;
- `healthcheck.sh` — скрипт проверки здоровья API;

Сгенерированный результат самодостаточен:
```bash
cd generated/<case>
cp infra/.env.example .env   # при необходимости
docker compose -f infra/docker-compose.yml up --build
```

Миграции и сид выполняются PostGIS-контейнером при первом старте
(`db/migrations/`, `db/seed/`).

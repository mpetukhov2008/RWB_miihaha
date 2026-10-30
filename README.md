# AI-Pipeline

Универсальный ИИ-пайплайн разработки: бизнес-требования → артефакты
проектирования → код, тесты, инфраструктура и документация.

Модель — локальная корпоративная Qwen (OpenAI-совместимый endpoint), работает
без интернета. Модель НЕ запускает инструменты — все сборки, тесты, сканеры
и запись файлов выполняет детерминированный Python-код пайплайна.

## Быстрый старт

```bash
pip install -e ".[dev]"

# Демо на FakeLLM (без сети и ключа):
LLM_MODE=mock ./run_pipeline.sh cases/parking/requirements.md
# или:
LLM_MODE=mock python -m pipeline.main run --requirements cases/parking/requirements.md

# Реальный прогон:
export LLM_BASE_URL=... LLM_API_KEY=... LLM_MODEL=...
./run_pipeline.sh cases/parking/requirements.md
```

Результат прогона — в `generated/<case>/`: артефакты, код, инфраструктура,
отчёты, `reports/usage.json` (токены/время/обращения).

## Переменные окружения

См. `.env.example`: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`,
`LLM_JSON_MODE`, `LLM_MODE` (mock для демо/CI), `DATABASE_URL`.

## Как устроен пайплайн

- `pipeline/orchestrator/` — порядок этапов, состояние, кэш, retry, Question Gate.
- `pipeline/agents/NN_name/` — агенты: `prompt.md`, `schema.json`, `checklist.md`.
- `schemas/` — JSON-контракты между этапами (общие для всех потребителей).
- `templates/` — заготовки стека (backend .NET, frontend Angular, geo, mocks, infra, ci).
- `cases/` — входные требования и эталоны кейсов.
- `generated/<case>/` — самодостаточный результат прогона.
- `reports/` — сводные отчёты (токены/время/попытки).

Подробнее: `docs/pipeline-architecture.md`.

## Тесты

```bash
make test        # pytest без сети (FakeLLM)
make lint        # ruff + mypy
make run-case1   # демо-прогон на FakeLLM
```

## Ограничения

- Пайплайн генерирует артефакты и код; реальная эксплуатация продукта —
  отдельная задача.
- Шаблоны (.NET/Angular) — рабочие каркасы, не production-grade.

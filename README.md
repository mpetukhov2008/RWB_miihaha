# AI-Pipeline

Универсальный ИИ-пайплайн разработки: бизнес-требования → артефакты
проектирования → код, тесты, инфраструктура и документация.

Модель — локальная корпоративная Qwen (OpenAI-совместимый endpoint), работает
без интернета. Модель НЕ запускает инструменты — все сборки, тесты, сканеры
и запись файлов выполняет детерминированный Python-код пайплайна.

## Быстрый старт

```bash
make install

# Демо на FakeLLM (без сети и ключа) — полный конвейер 01–09:
LLM_MODE=mock ./run_pipeline.sh cases/parking/requirements.md
# или с ответами на blocking-вопросы:
LLM_MODE=mock python -m pipeline.main run \
  --requirements cases/parking/requirements.md \
  --answers cases/parking/answers.json

# Реальный прогон:
export LLM_BASE_URL=... LLM_API_KEY=... LLM_MODEL=...
./run_pipeline.sh cases/parking/requirements.md
```

Результат — в `generated/parking/` (самодостаточен):

```
generated/parking/
├── 01_requirements/requirements.json
├── 02_system_analysis/system-analysis.md
├── 03_architecture_api/ (openapi.yaml, data-model.json, events.json, architecture.md)
├── 04_ui_design/ui-spec.json
├── 05_codegen_backend/backend/ (контроллеры, DTO, сущности .NET)
├── 06_codegen_frontend/frontend-admin/ (экраны, маршруты, API-сервис Angular)
├── 07_tests/ (api-tests.json, e2e-tests.json, test-report.md)
├── 08_security_report/reports/security-report.md
├── 09_docs/docs/ (README, user-guide, known-limitations, ...)
├── reports/ (usage.json — токены/время; traceability.md — матрица)
└── state.json (статусы этапов, возобновляемость)
```

## Переменные окружения

См. `.env.example`: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`,
`LLM_JSON_MODE`, `LLM_MODE` (mock — без сети), `DATABASE_URL`.

## Как устроен пайплайн

Этапы (один этап = один агент = один артефакт):

| # | Этап | Артефакт |
|---|---|---|
| 01 | requirements | `requirements.json` |
| 02 | system_analysis | `system-analysis.md` |
| 03 | architecture_api | `openapi.yaml`, `data-model.json`, `events.json`, `architecture.md` |
| 04 | ui_design | `ui-spec.json` |
| 05 | codegen_backend | backend .NET (контроллеры/DTO/сущности) |
| 06 | codegen_frontend | Angular (экраны/маршруты/API-сервис) |
| 07 | tests | api/e2e тесты + test-report |
| 08 | security_report | security-report.md |
| 09 | docs | документация |

Механика: кэш по sha256-хэшу запроса, retry (сетевой — 2 попытки, валидация —
retry с текстом ошибки), Question Gate (blocking-вопросы останавливают прогон
до `answers.json`, exit code 2), возобновляемость через `state.json`.

Подробнее: `docs/pipeline-architecture.md`, `CLAUDE.md` (правила агентов).

## Как добавить новый этап

4 файла + 1 строка: см. `docs/how-to-add-an-agent.md`.

## Метрики

После прогона: `generated/<case>/reports/usage.json` — токены (in/out),
время, вызовы, retry, cache hits по этапам; `reports/traceability.md` —
матрица «требование → API → экран → тест → документация».

## Тесты

```bash
make test        # pytest без сети (FakeLLM)
make lint        # ruff + mypy
make run-case1   # демо-прогон на FakeLLM
```

## Ограничения

- Шаблоны (.NET/Angular) — рабочие каркасы; сборка результата требует
  .NET 10 SDK и Node 22 (в CI сгенерированного проекта).
- Mock-оплата — имитация; реальная платёжная интеграция вне скоупа.
- Тесты самого пайплайна не требуют сети; e2e сгенерированного проекта —
  Playwright, запускается в его CI.

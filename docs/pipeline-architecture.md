# Архитектура пайплайна

## Принципы

1. Один этап = один агент = один артефакт.
2. Схема важнее промпта: валидация Pydantic, retry с текстом ошибки.
3. Модель ничего не запускает: сборка/тесты/сканеры/запись файлов — Python.
4. Всё на диск: `generated/<case>/`, состояние и кэш по хэшу запроса.
5. Тесты без модели: FakeLLM, 80% кода покрыто без токенов и сети.
6. Секретов в репозитории нет: только `.env.example` и CI variables.

## Этапы (агенты)

| # | Этап | Артефакты | Схема |
|---|---|---|---|
| 01 | requirements | `requirements.json` | `schemas/requirements.schema.json` |
| 02 | system_analysis | `system-analysis.md` | — (markdown по регламенту) |
| 03 | architecture_api | `openapi.yaml`, `data-model.json`, `events.json`, `architecture.md` | `schemas/data-model.schema.json`, `schemas/events.schema.json` |
| 04 | ui_design | `ui-spec.json` | `schemas/ui-spec.schema.json` |
| 05 | codegen_backend | решение .NET, тесты | OpenAPI → шаблон |
| 06 | codegen_frontend | Angular-приложение | ui-spec + ui-kit-rules |
| 07 | tests | e2e (Playwright), api-тесты | требования → критерии приёмки |
| 08 | security_report | `reports/security-report.md` | — |
| 09 | docs | docs/*.md | — |

## Ядро

- `pipeline/llm/` — клиент Qwen: кэш (sha256), JSONL-логи метрик, сетевые retry,
  mock-режим.
- `pipeline/orchestrator/` — `RunState` (state.json), `run_pipeline` (STAGES,
  Question Gate, персист артефактов, возобновляемость).
- `pipeline/validators/` — проверки артефактов: schema, уникальность ID,
  покрытие must-FR, OpenAPI-структура.
- `pipeline/profilers/` — профилировщик входных данных (`data-profile.json`).

## Поток

```
requirements.md
  └─> 01 requirements ──> 02 system_analysis ──> 03 architecture_api
        └─> 04 ui_design ──> 05 codegen_backend ──> 06 codegen_frontend
        └─> 07 tests ──> 08 security_report ──> 09 docs
  └─> generated/<case>/ (+ reports/usage.json, reports/traceability.md)
```

Blocking-вопросы останавливают прогон до появления `answers.json`.

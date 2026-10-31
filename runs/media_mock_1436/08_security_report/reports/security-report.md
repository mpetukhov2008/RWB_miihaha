# Security Report

Секретов в репозитории нет; JWT и rate limit настроены.

## Findings
| Severity | Title | Status | Description |
|---|---|---|---|
| info | JWT signing key по умолчанию | mitigated | В dev-конфигурации ключ задаётся через переменную окружения; в проде — через CI variables. |
| low | Rate limit 100 req/min — единый для всех | open | Для админ-операций можно ужесточить лимит. |

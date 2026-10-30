# Как добавить новый этап (агент)

Новый этап = 4 файла + 1 строка в оркестраторе.

## 1. Директория агента

Создай `pipeline/agents/NN_name/`:

| Файл | Назначение |
|---|---|
| `prompt.md` | Системный промпт: роль, задача этапа (и что НЕ входит), правила, «верни ТОЛЬКО JSON», ссылка на `checklist.md` |
| `checklist.md` | Чек-лист самопроверки модели |
| `schema.json` | JSON Schema артефакта (контракт для следующих этапов) |

## 2. Код агента

Создай `pipeline/agents/name.py`:

```python
from pipeline.agents.base import AgentResult, BaseAgent

class MyAgent(BaseAgent[dict]):
    name = "10_my_stage"
    prompt_version = "v1"

    def json_schema(self):
        return {...}  # или json.load(open("pipeline/agents/10_my_stage/schema.json"))

    def build_user_prompt(self, inputs: dict) -> str:
        # inputs содержит артефакты предыдущих этапов
        ...

    def validate(self, data, inputs) -> AgentResult:
        # 1) валидация pydantic/схемой
        # 2) gates: {"gate_name": "ok"|"fail"}
        # 3) артефакты: {"file.json": content}
        ...
```

## 3. Регистрация в оркестраторе

Добавь в `pipeline/orchestrator/orchestrator.py`:

```python
from pipeline.agents.my_stage import MyAgent

STAGES = [
    ...,
    ("10_my_stage", MyAgent),
]
```

## 4. Входные данные

В `_build_inputs` (там же) прочитай артефакты предыдущих этапов и положи
в `inputs` (например, `inputs["my_prev"] = _read_json(...)`).

## 5. Тесты

Минимум 2 теста (happy path + negative по gates) в `tests/` c `FakeLLM`
(без сети, без токенов): см. `tests/test_tests_agent.py` как образец.

## 6. Mock-ответ

Добавь предзаданный ответ в `pipeline/llm/mock.py` под ключом `10_my_stage`,
чтобы демо `LLM_MODE=mock` проходило весь конвейер.

## Правила

- Один этап = один агент = один артефакт.
- Схема важнее промпта: валидация → retry с текстом ошибки.
- Модель ничего не запускает; запись файлов — код пайплайна.
- В `pipeline/` и `templates/` не должно быть слов конкретного кейса.

"""Конфигурация пайплайна: env-переменные, пути, константы.

Все пути строятся от корня репозитория через :mod:`pathlib`, чтобы прогоны
были воспроизводимы независимо от текущей директории.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Корень репозитория: pipeline/config.py -> pipeline/ -> repo root.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Директории артефактов и промптов.
RUNS_DIR: Path = BASE_DIR / "runs"  # временные прогоны (не коммитятся)
GENERATED_DIR: Path = BASE_DIR / "generated"  # самодостаточный результат
CASES_DIR: Path = BASE_DIR / "cases"
SCHEMAS_DIR: Path = BASE_DIR / "schemas"
TEMPLATES_DIR: Path = BASE_DIR / "templates"
PROMPTS_DIR: Path = BASE_DIR / "pipeline" / "agents"  # NN_name/prompt.md
EXAMPLES_DIR: Path = BASE_DIR / "examples"

# Директории внутри одного прогона.
RUN_ARTIFACTS_DIRNAME = "artifacts"
RUN_CACHE_DIRNAME = "cache"
RUN_LOGS_DIRNAME = "logs"
RUN_METRICS_DIRNAME = "metrics"
RUN_TRACE_DIRNAME = "traceability"

# Количество попыток вызова LLM (retry) при ошибках сети/таймаута.
LLM_NETWORK_RETRIES = 2
# Таймаут одного вызова LLM, секунд.
LLM_TIMEOUT_SEC = 600

# Формат метки времени по умолчанию для run_id.
RUN_ID_FORMAT = "%Y%m%d-%H%M%S"


def load_env() -> None:
    """Загрузить переменные окружения из ``.env``, если файл существует."""
    load_dotenv(BASE_DIR / ".env")


class Settings:
    """Доступ к переменным окружения с дефолтами.

    Читает значения лениво, поэтому тесты могут подменять ``os.environ``
    без пересоздания объекта.
    """

    @property
    def llm_base_url(self) -> str:
        """Базовый URL OpenAI-совместимого endpoint."""
        return os.getenv("LLM_BASE_URL", "https://llm.example.local/v1")

    @property
    def llm_api_key(self) -> str:
        """API-ключ для доступа к модели."""
        return os.getenv("LLM_API_KEY", "")

    @property
    def llm_model(self) -> str:
        """Имя модели."""
        return os.getenv("LLM_MODEL", "qwen2.5-72b-instruct")

    @property
    def llm_json_mode(self) -> bool:
        """Использовать ли ``response_format={"type": "json_object"}``."""
        return os.getenv("LLM_JSON_MODE", "1") == "1"

    @property
    def llm_mode(self) -> str:
        """Режим LLM: ``mock`` — FakeLLM без сети, иначе — реальный клиент."""
        return os.getenv("LLM_MODE", "").strip().lower()

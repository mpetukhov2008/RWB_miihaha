"""Собственные исключения пайплайна."""


class PipelineError(Exception):
    """Базовое исключение пайплайна."""


class ValidationFailed(PipelineError):
    """Артефакт, полученный от модели, не прошёл валидацию схемы или gates."""


class StageFailed(PipelineError):
    """Этап пайплайна завершился ошибкой (исключение модели, gates и т.п.)."""


class LLMUnavailable(PipelineError):
    """LLM-клиент недоступен: ошибки сети, таймауты, неверный ключ."""

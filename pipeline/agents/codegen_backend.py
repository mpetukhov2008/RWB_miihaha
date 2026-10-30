"""Codegen Backend-агент: генерирует backend из артефактов.

Сначала пытается получить файлы от LLM (бизнес-логика, сервисы), затем
накладывает детерминированный каркас из OpenAPI/артефактов (контроллеры,
DTO, сущности), чтобы результат был гарантированно рабочим.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.generators.backend import build_backend_skeleton


class CodegenBackendAgent(BaseAgent[dict[str, Any]]):
    """Агент генерации backend.

    Attributes:
        name: Имя этапа — ``05_codegen_backend``.
    """

    name = "05_codegen_backend"
    prompt_version = "v1"
    # Схема ответа LLM: словарь файлов (используется в промпте, не в схеме).
    _FILE_SCHEMA = {
        "type": "object",
        "required": ["summary", "files"],
        "properties": {
            "summary": {"type": "string"},
            "files": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["path", "content"],
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                },
            },
        },
    }

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema ответа (files)."""
        return self._FILE_SCHEMA

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: openapi + architecture + схема."""
        openapi = inputs.get("openapi", {})
        arch = inputs.get("architecture", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — OpenAPI и архитектура. Сгенерируй backend-файлы.\n\n"
            f"=== OPENAPI.YAML ===\n{json.dumps(openapi, ensure_ascii=False, indent=2)}\n\n"
            f"=== ARCHITECTURE.JSON ===\n{json.dumps(arch, ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ LLM + наложить детерминированный каркас.

        Args:
            data: Ответ LLM (summary, files).
            inputs: Входные данные (openapi, architecture).

        Returns:
            AgentResult с файлами backend как артефактами.
        """
        llm_files: dict[str, str] = {}
        for f in data.get("files") or []:
            llm_files[f["path"]] = f["content"]

        # Детерминированный каркас (всегда).
        openapi = inputs.get("openapi") or {}
        arch = inputs.get("architecture") or {}
        ops = arch.get("operations") or []
        entities = arch.get("entities") or []
        skeleton = build_backend_skeleton(openapi, ops, entities)

        # Слияние: каркас — основа, LLM-файлы перекрывают (сервисы и т.п.).
        files = {**skeleton, **llm_files}

        artifacts: dict[str, Any] = {}
        for path, content in files.items():
            artifacts[f"backend/{path}"] = content

        gates: dict[str, str] = {
            "schema": "ok",
            "files_nonempty": "ok" if files else "fail",
            "controllers_generated": (
                "ok" if any(p.endswith("Controller.cs") for p in files) else "fail"
            ),
        }
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)
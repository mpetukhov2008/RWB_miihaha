"""Architecture API-агент: системная модель -> API и модель данных.

Генерирует ``data-model.json`` и ``events.json`` из ответа LLM, а
``openapi.yaml`` и ``architecture.md`` — детерминированно кодом.
"""

from __future__ import annotations

import json
from typing import Any

import yaml

from pipeline.agents.base import AgentResult, BaseAgent
from pipeline.schemas.architecture import ApiOperation, ArchitectureApi


class ArchitectureApiAgent(BaseAgent[ArchitectureApi]):
    """Агент архитектуры и API.

    Attributes:
        name: Имя этапа — ``03_architecture_api``.
    """

    name = "03_architecture_api"
    prompt_version = "v1"

    def json_schema(self) -> dict[str, Any]:
        """JSON Schema артефакта архитектуры."""
        return ArchitectureApi.model_json_schema()

    def build_user_prompt(self, inputs: dict[str, Any]) -> str:
        """Собрать user-промпт: requirements + system-model + схема.

        Args:
            inputs: Входные данные с ключами ``requirements`` и
                ``system_model`` (или ``system_analysis``).

        Returns:
            Текст user-промпта.
        """
        requirements = inputs.get("requirements", {})
        system_model = inputs.get("system_analysis", {})
        schema = json.dumps(self.json_schema(), ensure_ascii=False, indent=2)
        return (
            "Ниже — артефакты требований и системного анализа. "
            "Спроектируй модель данных, события и операции API.\n\n"
            f"=== REQUIREMENTS.JSON ===\n{json.dumps(requirements, ensure_ascii=False, indent=2)}\n\n"
            f"=== SYSTEM-ANALYSIS ===\n{json.dumps(system_model, ensure_ascii=False, indent=2)}\n\n"
            f"=== JSON SCHEMA ОТВЕТА ===\n{schema}\n"
        )

    def validate(self, data: dict[str, Any], inputs: dict[str, Any]) -> AgentResult:
        """Валидировать ответ: схема + gates + детерминированные артефакты.

        Args:
            data: Ответ модели.
            inputs: Входные данные (требования).

        Returns:
            AgentResult с артефактами:
            ``data-model.json``, ``events.json``, ``openapi.yaml``,
            ``architecture.md`` — и gates.
        """
        model = ArchitectureApi.model_validate(data)

        openapi = self._build_openapi(model)

        # Gates.
        gates: dict[str, str] = {}
        gates["schema"] = "ok"
        # У каждой операции есть operationId и tags.
        gates["operation_ids"] = (
            "ok"
            if all(op.operationId for op in model.operations)
            else "fail"
        )
        gates["tags_defined"] = (
            "ok"
            if all(op.tags for op in model.operations)
            else "fail"
        )
        # Единый формат ошибок.
        gates["error_format"] = (
            "ok"
            if all(op.error_schema == "ProblemDetails" for op in model.operations)
            else "fail"
        )
        # Покрытие must-FR (по requirements.json).
        requirements = inputs.get("requirements", {})
        must_ids = [
            r["id"]
            for r in requirements.get("requirements", [])
            if r.get("priority") == "must"
        ]
        covered: set[str] = set()
        for op in model.operations:
            covered.update(op.requirement_ids)
        missing = [rid for rid in must_ids if rid not in covered]
        gates["must_coverage"] = "ok" if not missing else "fail"

        artifacts = {
            "data-model.json": json.loads(
                json.dumps([e.model_dump() for e in model.entities], ensure_ascii=False)
            ),
            "events.json": json.loads(
                json.dumps([e.model_dump() for e in model.events], ensure_ascii=False)
            ),
            "openapi.yaml": openapi,
            "architecture.md": self._render_architecture(model),
            "architecture.json": json.loads(model.model_dump_json()),
        }
        return AgentResult(artifacts=artifacts, gates=gates, questions_blocking=0)

    @staticmethod
    def _build_openapi(model: ArchitectureApi) -> str:
        """Собрать OpenAPI 3.1.0 документ (детерминированно).

        Args:
            model: Валидная архитектурная модель.

        Returns:
            YAML-текст openapi.yaml с расширением ``x-requirement-ids``.
        """
        paths: dict[str, Any] = {}
        for op in model.operations:
            path_item = paths.setdefault(op.path, {})
            responses: dict[str, Any] = {}
            if op.errors:
                for code in op.errors:
                    responses[code] = {
                        "description": "Ошибка",
                        "content": {
                            "application/problem+json": {
                                "schema": {"$ref": "#/components/schemas/ProblemDetails"}
                            }
                        },
                    }
            operation: dict[str, Any] = {
                "operationId": op.operationId,
                "summary": op.summary,
                "tags": op.tags,
                "x-requirement-ids": op.requirement_ids,
                "responses": responses,
            }
            if op.request_schema:
                operation["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {"schema": op.request_schema}
                    },
                }
            if op.auth:
                operation["security"] = [{"bearerAuth": []}]
            path_item[op.method] = operation

        doc: dict[str, Any] = {
            "openapi": "3.1.0",
            "info": {
                "title": "API",
                "version": "1.0.0",
                "description": "Сгенерировано из системной модели",
            },
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "bearerAuth": {"type": "http", "scheme": "bearer"}
                },
                "schemas": {
                    "ProblemDetails": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "title": {"type": "string"},
                            "status": {"type": "integer"},
                            "detail": {"type": "string"},
                            "instance": {"type": "string"},
                        },
                    }
                },
            },
        }
        return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)

    @staticmethod
    def _render_architecture(model: ArchitectureApi) -> str:
        """Собрать ``architecture.md`` (детерминированно).

        Args:
            model: Валидная архитектурная модель.

        Returns:
            Текст architecture.md.
        """
        lines = ["# Архитектура", ""]
        lines.append("## Модель данных")
        for e in model.entities:
            lines.append(f"### {e.name}")
            lines.append(e.description)
            for f in e.fields:
                req = " (required)" if f.required else ""
                lines.append(f"- `{f.name}`: `{f.type}`{req} — {f.description}")
            lines.append("")
        lines.append("## События")
        for ev in model.events:
            lines.append(f"- **{ev.name}** v{ev.version}: {ev.description}")
        lines.append("")
        lines.append("## API")
        for op in model.operations:
            auth = " (auth)" if op.auth else ""
            lines.append(
                f"- `{op.method.upper()} {op.path}` — {op.operationId}{auth}"
            )
            if op.requirement_ids:
                lines.append(f"  - требования: {', '.join(op.requirement_ids)}")
        return "\n".join(lines).strip() + "\n"
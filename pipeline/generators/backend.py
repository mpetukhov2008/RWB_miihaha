"""Детерминированная генерация backend (.NET) из OpenAPI/артефактов.

Строит контроллеры и DTO из операций OpenAPI без LLM. Это дополняет
агента 05 (LLM даёт бизнес-логику, генератор — каркас).
"""

from __future__ import annotations

from typing import Any

# Соответствие OpenAPI-методов HTTP-глаголам C#.
_METHOD_ATTR = {
    "get": "HttpGet",
    "post": "HttpPost",
    "put": "HttpPut",
    "patch": "HttpPatch",
    "delete": "HttpDelete",
}


def _pascal(name: str) -> str:
    """Преобразовать строку в PascalCase."""
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_"))


def _dto_name(schema: dict[str, Any] | None, fallback: str) -> str:
    """Имя DTO из $ref или fallback."""
    if not schema:
        return fallback
    ref = schema.get("$ref", "")
    if ref:
        return ref.rsplit("/", 1)[-1]
    return fallback


def build_backend_skeleton(
    openapi: dict[str, Any],
    operations: list[dict[str, Any]],
    entities: list[dict[str, Any]],
) -> dict[str, str]:
    """Собрать каркас backend-проекта из OpenAPI и модели данных.

    Args:
        openapi: Распарсенный openapi.yaml.
        operations: Операции (из architecture.json).
        entities: Модель данных (data-model.json).

    Returns:
        Словарь «путь -> содержимое файла» (controllers, DTO, entities).
    """
    files: dict[str, str] = {}

    # Группируем операции по tags (по одному контроллеру на tag).
    by_tag: dict[str, list[dict[str, Any]]] = {}
    for op in operations:
        for tag in op.get("tags") or ["default"]:
            by_tag.setdefault(tag, []).append(op)

    for tag, ops in by_tag.items():
        controller_name = _pascal(tag) + "Controller"
        lines = [
            "using Generated.Api.Common;",
            "using Generated.Api.Data;",
            "using Microsoft.AspNetCore.Authorization;",
            "using Microsoft.AspNetCore.Mvc;",
            "namespace Generated.Api.Controllers;",
            "",
            "[ApiController]",
            f'[Route("api/{tag}")]',
            f"public class {controller_name}(AppDbContext db) : ControllerBase",
            "{",
        ]
        for op in ops:
            method = _pascal(op.get("operationId", "op"))
            http_attr = _METHOD_ATTR.get(op.get("method", "get"), "HttpGet")
            route = op.get("path", "/").replace(f"/{tag}", "", 1) or "/"
            lines.append("")
            lines.append(f"    /// <summary>{op.get('summary', '')}</summary>")
            if op.get("auth"):
                lines.append("    [Authorize]")
            if route in ("/", ""):
                lines.append(f"    [{http_attr}]")
            else:
                lines.append(f'    [{http_attr}("{route.lstrip("/")}")]')
            lines.append(f"    public IActionResult {method}()")
            lines.append("    {")
            lines.append("        // TODO: бизнес-логика (агент 05/сервисы).")
            lines.append(f'        return Ok(new {{ Operation = "{op.get("operationId")}" }});')
            lines.append("    }")
        lines.append("}")
        files[f"Controllers/{controller_name}.cs"] = "\n".join(lines) + "\n"

    # DTO из request/response схем.
    for op in operations:
        req = op.get("request_schema")
        if req:
            name = _dto_name(req, _pascal(op.get("operationId", "op")) + "Request")
            files[f"Dtos/{name}.cs"] = _dto_class(name, req)
        res = op.get("response_schema")
        if res and "$ref" in res:
            name = res["$ref"].rsplit("/", 1)[-1]
            files[f"Dtos/{name}.cs"] = _dto_class(
                name, {"type": "object", "properties": {"id": {"type": "string"}}}
            )

    # EF-сущности из data-model.json.
    for ent in entities:
        name = _pascal(ent.get("name", "Entity"))
        files[f"Entities/{name}.cs"] = _entity_class(name, ent)

    return files


def _dto_class(name: str, schema: dict[str, Any]) -> str:
    """C# record-класс DTO из JSON-схемы."""
    lines = [
        "namespace Generated.Api.Dtos;",
        "",
        f"public record {name}",
        "(",
    ]
    props: list[str] = []
    for pname, ptype in (schema.get("properties") or {}).items():
        props.append(f"    {_pascal(pname)} {_cs_type(ptype)}")
    if not props:
        props = ["    object Payload"]
    lines.append(",\n".join(props))
    lines.append(");")
    return "\n".join(lines) + "\n"


def _entity_class(name: str, ent: dict[str, Any]) -> str:
    """C# EF-сущность из data-model.json."""
    lines = [
        "namespace Generated.Api.Entities;",
        "",
        f"public class {name}",
        "{",
    ]
    fields: list[str] = []
    for f in ent.get("fields") or []:
        fname = _pascal(f.get("name", "Id"))
        cs = _cs_type({"type": f.get("type", "string")})
        default = ' = string.Empty;' if cs == "string" else ""
        if fname == "Id" and "Guid" not in cs:
            cs = "Guid"
        fields.append(f"    public {cs} {fname} {{ get; set; }}{default}")
    if not fields:
        fields = ["    public Guid Id { get; set; }"]
    lines.extend(fields)
    lines.append("}")
    return "\n".join(lines) + "\n"


def _cs_type(schema: dict[str, Any]) -> str:
    """Маппинг JSON-типа в C#."""
    t = schema.get("type", "string")
    if t == "string":
        return "string"
    if t in ("integer", "number"):
        return "decimal"
    if t == "boolean":
        return "bool"
    if t == "array":
        return "List<object>"
    return "object"
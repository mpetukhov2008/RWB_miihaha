"""Детерминированная генерация frontend (Angular) из ui-spec/OpenAPI.

Строит экраны, компоненты, маршруты и API-сервисы из артефактов без LLM.
"""

from __future__ import annotations

from typing import Any


def _pascal(name: str) -> str:
    """Преобразовать строку в PascalCase."""
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_"))


def _kebab(name: str) -> str:
    """Преобразовать строку в kebab-case."""
    return "".join("-" + c.lower() if c.isupper() else c for c in name).lstrip("-")


def build_frontend_skeleton(
    ui_spec: dict[str, Any],
    operations: list[dict[str, Any]],
) -> dict[str, str]:
    """Собрать Angular-каркас из ui-spec и операций.

    Args:
        ui_spec: ui-spec.json.
        operations: Операции (из architecture.json).

    Returns:
        Словарь «путь -> содержимое файла».
    """
    files: dict[str, str] = {}

    screens = ui_spec.get("screens") or []
    for screen in screens:
        scr_id = screen.get("id", "SCR-000")
        name = _pascal(scr_id)
        files[f"screens/{scr_id}/{name}.component.ts"] = _screen_component(scr_id, screen)

    files["app/app.routes.ts"] = _routes(screens)
    files["app/services/api.service.ts"] = _api_service(operations)

    return files


def _screen_component(scr_id: str, screen: dict[str, Any]) -> str:
    """Angular-компонент экрана (состояния из ui-spec)."""
    title = screen.get("title", scr_id)
    states = screen.get("states") or {}
    actions = screen.get("actions") or []

    action_html = "".join(
        f'<button mat-raised-button (click)="run(\'{a.get("api_operation_id", "")}\')">'
        f'{a.get("label", "OK")}</button>\n'
        for a in actions
    )

    states_block = "".join(
        f"@if (state === '{key}') {{ <div class=\"state\">{value}</div> }}\n"
        for key, value in states.items()
        if value
    )

    return f"""import {{ Component }} from '@angular/core';
import {{ MatButtonModule }} from '@angular/material/button';
import {{ MatProgressSpinnerModule }} from '@angular/material/progress-spinner';
import {{ ApiService }} from '../services/api.service';

@Component({{
  selector: 'app-{_kebab(scr_id)}',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>{title}</h2>
    {states_block}
    {action_html}
  `,
  styles: [`.state {{ padding: 1rem; }}`],
}})
export class {_pascal(scr_id)}Component {{
  state = 'loading';
  constructor(private api: ApiService) {{
    setTimeout(() => (this.state = 'success'), 300);
  }}
  run(operationId: string) {{
    this.api.call(operationId).subscribe({{
      next: () => (this.state = 'success'),
      error: () => (this.state = 'error'),
    }});
  }}
}}
"""


def _routes(screens: list[dict[str, Any]]) -> str:
    """Маршруты Angular из экранов."""
    lines = [
        "import { Routes } from '@angular/router';",
        "import { HomeComponent } from './home/home.component';",
    ]
    for screen in screens:
        scr_id = screen.get("id", "SCR-000")
        name = _pascal(scr_id)
        lines.append(
            f"import {{ {name}Component }} from './screens/{scr_id}/{name}.component';"
        )
    lines.append("")
    lines.append("export const routes: Routes = [")
    lines.append("  { path: '', component: HomeComponent },")
    for screen in screens:
        scr_id = screen.get("id", "SCR-000")
        name = _pascal(scr_id)
        lines.append(f"  {{ path: '{_kebab(scr_id)}', component: {name}Component }},")
    lines.append("  { path: '**', redirectTo: '' },")
    lines.append("];")
    return "\n".join(lines) + "\n"


def _api_service(operations: list[dict[str, Any]]) -> str:
    """API-сервис Angular из операций."""
    lines = [
        "import { Injectable } from '@angular/core';",
        "import { HttpClient } from '@angular/common/http';",
        "import { Observable } from 'rxjs';",
        "",
        "@Injectable({ providedIn: 'root' })",
        "export class ApiService {",
        "  constructor(private http: HttpClient) {}",
        "",
        "  call(operationId: string): Observable<unknown> {",
        "    const map: Record<string, { method: string; path: string }> = {",
    ]
    for op in operations:
        method = op.get("method", "get").upper()
        path = op.get("path", "/")
        lines.append(f"      '{op.get('operationId')}': {{ method: '{method}', path: '{path}' }},")
    lines.extend([
        "    };",
        "    const op = map[operationId];",
        "    if (!op) return new Observable((s) => s.error(new Error('unknown op')));",
        "    return this.http.request(op.method, op.path);",
        "  }",
        "}",
    ])
    return "\n".join(lines) + "\n"
#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
RUN="${1:-runs/media_fixed2_1507}"

echo "════════════════════════════════════════════════════════════"
echo "  DEMO: реальный прогон qwen3.8-27b, 9/9 этапов, EXIT 0"
echo "════════════════════════════════════════════════════════════"
echo
echo "▸ ЭТАПЫ:"
cat "$RUN/state.json" | python -c "import json,sys; d=json.load(sys.stdin); [print(f'  {k:24} {v[\"status\"]:8}') for k,v in d['stages'].items()]"
echo
echo "▸ ВАЛИДАЦИЯ API:"
npx --yes @redocly/cli lint "$RUN/03_architecture_api/openapi.yaml" 2>&1 | tail -3
echo
echo "▸ API-ДОКИ: /tmp/api-docs.html ($(stat -c%s /tmp/api-docs.html) байт)"
echo
echo "▸ ЭНДПОИНТЫ:"
python - "$RUN/03_architecture_api/openapi.yaml" << 'PY'
import sys, yaml
spec = yaml.safe_load(open(sys.argv[1]))
for path, methods in spec.get("paths", {}).items():
    for m, op in methods.items():
        if m.lower() in ("get","post","put","patch","delete"):
            print(f"  {m.upper():6} {path:40} {op.get('x-requirement-ids', [])}")
PY
echo
echo "▸ АРТЕФАКТЫ:"
echo "  backend .cs: $(find "$RUN/05_codegen_backend" -name '*.cs' | wc -l)"
echo "  frontend .ts: $(find "$RUN/06_codegen_frontend" -name '*.ts' | wc -l)"
echo "  tests: $(ls "$RUN/07_tests/tests/" | tr '\n' ' ')"
echo "  docs: $(ls "$RUN/09_docs/docs/" | tr '\n' ' ')"

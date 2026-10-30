#!/usr/bin/env bash
# Один вход: ./run_pipeline.sh <кейс>/requirements.md
# Результат всегда попадает в generated/<кейс>/.
set -euo pipefail

REQUIREMENTS="${1:?Usage: ./run_pipeline.sh <path/to/requirements.md>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Запуск пайплайна для: $REQUIREMENTS"
python3 -m pipeline.main run --requirements "$REQUIREMENTS"

echo "==> Готово. Результат: generated/$(basename "$(dirname "$REQUIREMENTS")")/"

#!/usr/bin/env bash
# Один вход: ./run_pipeline.sh <кейс>/requirements.md
# Результат всегда попадает в generated/<кейс>/.
set -euo pipefail

# Гарантия UTF-8: на VM с C-локалью open()/stdout падают на кириллице
# ("ascii codec can't encode"). PYTHONUTF8=1 принудительно включает
# UTF-8 режим Python независимо от системной локали.
export PYTHONUTF8=1
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"

REQUIREMENTS="${1:?Usage: ./run_pipeline.sh <path/to/requirements.md>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Запуск пайплайна для: $REQUIREMENTS"
python3 -m pipeline.main run --requirements "$REQUIREMENTS"

echo "==> Готово. Результат: generated/$(basename "$(dirname "$REQUIREMENTS")")/"

#!/usr/bin/env bash
# Healthcheck для API в docker-compose.
set -euo pipefail
curl -fsS "${HEALTHCHECK_URL:-http://localhost:8080/health}" || exit 1

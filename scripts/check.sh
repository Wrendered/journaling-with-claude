#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
bash scripts/verify-sync.sh
bash scripts/public-sanity-check.sh

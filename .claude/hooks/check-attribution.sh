#!/usr/bin/env bash
# Compatibility entry point; shared implementation checks only the changed text.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 "$REPO_DIR/scripts/vault.py" hook

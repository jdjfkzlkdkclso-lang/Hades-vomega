#!/usr/bin/env bash
# HADES vOmega - Core
# Uso: hades_core.sh [help|version|status]

VERSION="1.0.0"
HADES_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cmd="${1:-help}"

case "$cmd" in
  version)
    echo "HADES vOmega v${VERSION}"
    ;;
  status)
    echo "[STATUS] Root: $HADES_ROOT"
    echo "[STATUS] Fecha: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "[STATUS] Shell: $BASH_VERSION"
    ;;
  help|*)
    echo "Uso: hades_core.sh [help|version|status]"
    ;;
esac

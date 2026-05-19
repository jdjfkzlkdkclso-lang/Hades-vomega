#!/usr/bin/env bash
# HADES vOmega - Smoke Test

PASS=0
FAIL=0

check() {
  local desc="$1"
  local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "[PASS] $desc"
    ((PASS++))
  else
    echo "[FAIL] $desc"
    ((FAIL++))
  fi
}

check "src/hades_core.sh existe"   "[ -f src/hades_core.sh ]"
check "hades_core.sh ejecutable"   "[ -x src/hades_core.sh ]"
check "README.md existe"           "[ -f README.md ]"
check "Directorio evidence existe" "[ -d evidence ]"

echo ""
echo "Resultado: ${PASS} PASS / ${FAIL} FAIL"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1

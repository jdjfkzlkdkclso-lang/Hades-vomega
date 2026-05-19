#!/bin/bash
set -euo pipefail
ERRORS=0
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  HADES vΩ - VERIFICACIÓN TOTAL DEL SISTEMA                       ║"
echo "╚══════════════════════════════════════════════════════════════════╝"

echo "[1/7] DIRECTORIOS..."
for dir in "$HOME/HADES_AGENTE_EVOLUTIVO" "$HOME/agentes_elite" "$HOME/HADES_FUSION_NUCLEO_vΩ/backup_014330/.leviatan_core/vault/agents"; do
    [ -d "$dir" ] && echo "✅ $dir" || { echo "❌ $dir"; ((ERRORS++)); }
done

echo "[2/7] ARCHIVOS JSON..."
for file in "$HOME/HADES_AGENTE_EVOLUTIVO/agente_evolutivo_v2.json" "$HOME/HADES_AGENTE_EVOLUTIVO/agente_evolutivo_v2_DIAMANTE_PURO.json"; do
    [ -f "$file" ] && echo "✅ $file" || { echo "❌ $file"; ((ERRORS++)); }
done

echo "[3/7] SINTAXIS JSON..."
python3 -c "import json; json.load(open('$HOME/HADES_AGENTE_EVOLUTIVO/agente_evolutivo_v2.json'))" && echo "✅ JSON válido" || { echo "❌ JSON corrupto"; ((ERRORS++)); }

echo "[4/7] ALIAS..."
for a in hades elite agentes hades-edit hades-ver hades-info hades-backup hades-restore; do
    alias | grep -q "alias $a=" && echo "✅ $a" || { echo "❌ $a"; ((ERRORS++)); }
done

echo "[5/7] VARIABLES..."
for v in HADES_AGENTE HADES_ELITE HADES_ORIGEN; do
    [ -n "${!v:-}" ] && echo "✅ $v" || { echo "❌ $v"; ((ERRORS++)); }
done

echo "[6/7] hades-info..."
hades-info 2>/dev/null && echo "✅ hades-info funciona" || { echo "❌ hades-info falló"; ((ERRORS++)); }

echo "[7/7] COHERENCIA..."
python3 -c "import json,sys; d=json.load(open('$HOME/HADES_AGENTE_EVOLUTIVO/agente_evolutivo_v2.json')); assert d['name']=='HADES_AGENTE_EVOLUTIVO_vΩ'; assert d['mode']=='DEPREDADOR⁹⁰'; assert d['ontology']['simulacion']=='0%'; assert len(d['nodes'])==5; print('✅ COHERENCIA ONTOLOGICA OK')" || { echo "❌ INCOHERENCIA"; ((ERRORS++)); }

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ VERIFICACIÓN TOTAL: 0 ERRORES"
    echo "👁️👁️ SISTEMA HADES vΩ OPERATIVO AL 100%"
else
    echo "❌ VERIFICACIÓN TOTAL: $ERRORS ERRORES"
fi

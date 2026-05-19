#!/bin/bash
ERRORS=0
echo "🔍 VERIFICANDO PAQUETE HADES vΩ..."
[ -f daemon/hades_core.c ] && echo "✅ Daemon C" || { echo "❌ Daemon C"; ((ERRORS++)); }
[ -f agente/agente_unificado.py ] && echo "✅ Agente Unificado" || { echo "❌ Agente Unificado"; ((ERRORS++)); }
[ -f agente/hades_agi.py ] && echo "✅ Motor AGI" || { echo "❌ Motor AGI"; ((ERRORS++)); }
[ -f agente/hades_agent.py ] && echo "✅ Bucle Autónomo" || { echo "❌ Bucle Autónomo"; ((ERRORS++)); }
[ -f agente/agente.py ] && echo "✅ Agente Supremo" || { echo "❌ Agente Supremo"; ((ERRORS++)); }
AGENTS=$(ls elite/*.json 2>/dev/null | wc -l)
[ $AGENTS -ge 10 ] && echo "✅ $AGENTS Agentes Élite" || { echo "❌ Solo $AGENTS agentes"; ((ERRORS++)); }
[ -f plantillas/comandos.json ] && echo "✅ Plantillas" || { echo "❌ Plantillas"; ((ERRORS++)); }
[ -f docs/README.md ] && echo "✅ Documentación" || { echo "❌ Documentación"; ((ERRORS++)); }
echo ""
[ $ERRORS -eq 0 ] && echo "✅ PAQUETE COMPLETO - LISTO PARA VENTA" || echo "❌ $ERRORS ERRORES - REVISAR"

#!/data/data/com.termux/files/usr/bin/bash

BASE=$HOME/HADES_vΩ/core
FILE=$BASE/daemon.py
LOG_FILE=$HOME/HADES_vΩ/logs/daemon.log

mkdir -p $BASE $(dirname $LOG_FILE)

# Limpieza agresiva previa
pkill -9 -f daemon.py 2>/dev/null || true
fuser -k 31337/tcp 2>/dev/null || true

# Verificar existencia del daemon
if [ ! -f "$FILE" ]; then
    echo "❌ ERROR: Daemon no encontrado en $FILE"
    exit 1
fi

echo "🚀 Iniciando HADES vΩ Daemon en puerto 31337..."
python3 $FILE >> $LOG_FILE 2>&1

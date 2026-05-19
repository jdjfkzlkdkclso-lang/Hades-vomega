#!/data/data/com.termux/files/usr/bin/sh
LOG="$HOME/HADES_vΩ/logs/supervisor.log"
DAEMON="$HOME/HADES_vΩ/core/daemon.py"

echo "[$(date)] Supervisor iniciado" >> $LOG

while true; do
    echo "[$(date)] Iniciando Daemon..." >> $LOG
    python3 "$DAEMON" >> "$HOME/HADES_vΩ/logs/daemon.log" 2>&1
    EXIT_CODE=$?
    echo "[$(date)] Daemon terminó con código $EXIT_CODE. Reiniciando en 3s..." >> $LOG
    sleep 3
done

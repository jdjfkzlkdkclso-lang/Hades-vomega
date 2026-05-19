#!/data/data/com.termux/files/usr/bin/bash
read -sp "[DEPREDADOR⁹⁰] Introduce MASTER_KEY: " MK
export HADES_MASTER_KEY=$MK
echo -e "\n[!] Ignición de Daemon..."
node hades_daemon.js >> ./logs/daemon.log 2>&1 &

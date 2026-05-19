# HADES vΩ COMPLETE ARSENAL
## Requisitos
- Termux (Android ARM64)
- Python 3.11+
- Clang (para compilar daemon)
## Instalación
cd daemon
clang -O3 -march=native -flto hades_core.c -o hades_daemon -lm
./hades_daemon hades_in.fifo hades_out.fifo &
cd ../agente
python3 agente_unificado.py
## Comandos JSON
{"action": "ping"}
{"action": "nucleo_info"}
{"action": "bash", "bash": "echo HADES ACTIVO"}
## Agentes Élite
Importa los archivos JSON de /elite en n8n.

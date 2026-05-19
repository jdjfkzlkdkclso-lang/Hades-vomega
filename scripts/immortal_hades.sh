#!/data/data/com.termux/files/usr/bin/bash
# HADES vΩ.97 - RUNTIME RECOVERY
export PREFIX="/data/data/com.termux/files/usr"
export PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
export PYTHONPATH="$PREFIX/lib/python$PY_VER/site-packages:$HOME/HADES_ORACLE"
export LD_LIBRARY_PATH="$PREFIX/lib"
export LD_PRELOAD="$PREFIX/lib/libpython$PY_VER.so"
export PYTHONNOUSERSITE=1

cd ~/HADES_ORACLE
echo "[!] DESPLEGANDO HADES vΩ.97..."
# Ejecución directa con supresión de warnings y buffer de salida forzado
python3 -u -W ignore enterprise_oracle.py

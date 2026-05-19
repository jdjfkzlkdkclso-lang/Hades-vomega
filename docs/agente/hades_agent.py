#!/usr/bin/env python3
"""
HADES AUTONOMOUS AGENT vΩ
Agente autónomo con sensores IPC y bucle de ejecución continua.
Se integra con AGI_Core_Architecture.js (PID 7156) vía FIFOs.
"""
import os
import time
import json
import select
import asyncio
from pathlib import Path

class C_ABI_Sensors:
    """Sensores de comunicación Inter-Proceso vía FIFOs."""
    def __init__(self):
        self.base = Path.home() / "HADES_AUTONOMOUS" / "tmp"
        self.pipe_in = self.base / "hades_in.fifo"
        self.pipe_out = self.base / "hades_out.fifo"
        
        # Verificar existencia de FIFOs
        for pipe in [self.pipe_in, self.pipe_out]:
            if not pipe.exists():
                print(f"[AUTONOMOUS] FIFO ausente: {pipe}. Reconstruyendo...")
                os.mkfifo(pipe, 0o666)
        
        self.fd_in = os.open(self.pipe_in, os.O_RDONLY | os.O_NONBLOCK)
        self.fd_out = os.open(self.pipe_out, os.O_WRONLY)
        print(f"[AUTONOMOUS] Sensores IPC inicializados")

    def read_signal(self) -> dict | None:
        """Lectura no bloqueante de señales entrantes."""
        try:
            ready, _, _ = select.select([self.fd_in], [], [], 0.1)
            if ready:
                data = os.read(self.fd_in, 4096)
                if data:
                    return json.loads(data.decode())
        except Exception as e:
            print(f"[AUTONOMOUS] Error lectura: {e}")
        return None

    def send_signal(self, payload: dict):
        """Envío de respuesta al bus IPC."""
        try:
            msg = json.dumps(payload) + "\n"
            os.write(self.fd_out, msg.encode())
        except Exception as e:
            print(f"[AUTONOMOUS] Error envío: {e}")

class AutonomousAgent:
    """Agente principal con bucle de razonamiento continuo."""
    def __init__(self):
        self.sensors = C_ABI_Sensors()
        self.state = {
            "status": "initializing",
            "protocol": "HADES_vΩ_AUTONOMOUS",
            "uptime": 0,
            "signals_processed": 0,
            "last_signal": None
        }
        self.run_flag = True
        print(f"[AUTONOMOUS] Agente inicializado")

    async def process_signal(self, signal: dict):
        """Procesamiento de señales entrantes."""
        action = signal.get("action", "ping")
        self.state["signals_processed"] += 1
        self.state["last_signal"] = signal
        
        if action == "ping":
            return {"status": "pong", "timestamp": time.time()}
        elif action == "system_status":
            return self.state
        elif action == "shutdown":
            self.run_flag = False
            return {"status": "shutting_down"}
        else:
            return {"status": "unknown_action", "action": action}

    async def execute(self):
        """Bucle principal de ejecución."""
        print(f"[AUTONOMOUS] Iniciando bucle de ejecución...")
        self.sensors.send_signal({
            "status": "online",
            "protocol": "HADES_vΩ_AUTONOMOUS",
            "timestamp": time.time()
        })
        
        while self.run_flag:
            signal = self.sensors.read_signal()
            if signal:
                response = await self.process_signal(signal)
                self.sensors.send_signal(response)
                self.state["uptime"] = time.time() - self.state.get("start_time", time.time())
            
            # Mantenimiento periódico
            if self.state["signals_processed"] % 100 == 0 and self.state["signals_processed"] > 0:
                self.sensors.send_signal({
                    "type": "heartbeat",
                    "signals": self.state["signals_processed"],
                    "uptime": self.state["uptime"]
                })
            
            await asyncio.sleep(0.01)  # 100Hz loop
        
        self.sensors.send_signal({"status": "offline"})
        print(f"[AUTONOMOUS] Agente detenido. Señales procesadas: {self.state['signals_processed']}")

if __name__ == "__main__":
    agente = AutonomousAgent()
    agente.state["start_time"] = time.time()
    try:
        asyncio.run(agente.execute())
    except KeyboardInterrupt:
        print("\n[AUTONOMOUS] Interrupción recibida. Apagando...")
    except Exception as e:
        print(f"[AUTONOMOUS] Error fatal: {e}")

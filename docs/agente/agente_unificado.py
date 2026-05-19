#!/usr/bin/env python3
import asyncio, aiohttp, json, os, struct, hashlib, time, sys, math, shlex
from pathlib import Path
from datetime import datetime

# ─── CONSTANTES ───────────────────────────────────────────────────
FRAME_SIZE  = 64
PIPE_IN     = os.path.expanduser("~/HADES_UNIFIED/tmp/hades_in.fifo")
PIPE_OUT    = os.path.expanduser("~/HADES_UNIFIED/tmp/hades_out.fifo")
SIG_HEX     = 0x48414445535F564F
FRAME_FMT   = "<QB47sQ"
HOME        = Path.home() / "HADES_UNIFIED"
NCPC        = hashlib.blake2b(b'HADES_UNIFIED_V90', digest_size=16).hexdigest()

# ─── PALETA ────────────────────────────────────────────────────────
VF='\033[1;38;5;46m'; AF='\033[1;38;5;226m'; AM='\033[1;38;5;27m'
CE='\033[1;38;5;51m'; RC='\033[1;38;5;196m'; MN='\033[1;38;5;201m'; RE='\033[0m'
def c(col, txt): return f"{col}{txt}{RE}"

# ─── MOTOR C-ABI ──────────────────────────────────────────────────
class HadesABIEngine:
    def __init__(self):
        fd_out_num = os.open(PIPE_IN, os.O_RDWR)
        fd_in_num  = os.open(PIPE_OUT, os.O_RDWR)
        self.fd_out = os.fdopen(fd_out_num, "wb", buffering=0)
        self.fd_in  = os.fdopen(fd_in_num, "rb", buffering=0)

    def invoke(self, opcode: int, data: bytes = b"") -> dict:
        payload = data[:47].ljust(47, b'\x00')
        trama = struct.pack(FRAME_FMT, SIG_HEX, opcode, payload, 0)
        t0 = time.perf_counter()
        self.fd_out.write(trama)
        resp = b""
        while len(resp) < FRAME_SIZE:
            chunk = self.fd_in.read(FRAME_SIZE - len(resp))
            if chunk: resp += chunk
        t1 = time.perf_counter()
        _, _, r_payload, r_seal = struct.unpack(FRAME_FMT, resp)
        return {
            "latencia_us": round((t1-t0)*1_000_000, 2),
            "sello_ncpc": hex(r_seal),
            "payload": r_payload.decode('utf-8', errors='ignore').strip('\x00')
        }

# ─── MEMORIA AGI ──────────────────────────────────────────────────
class AGI_Memory:
    def __init__(self):
        self.short_term = []
        self.weights = [0.1] * 1024
    def attention(self, query: str) -> dict:
        encoded = hashlib.md5(query.encode()).digest()
        score = sum(encoded[i%16] * self.weights[i] for i in range(1024))
        self.short_term.append({"q": query, "t": time.time(), "score": score})
        return {"atencion": score, "proyeccion": "1024D_LATENTE"}

# ─── ORÁCULO PREDICTIVO ───────────────────────────────────────────
class PredictiveOracle:
    @staticmethod
    def forecast(series: list) -> dict:
        if not series: return {"prediccion": 0}
        mean = sum(series)/len(series)
        vol  = math.sqrt(sum((x-mean)**2 for x in series)/len(series))
        return {"prediccion_t1": round(mean+vol*0.95, 4), "confianza": "95%"}

# ─── ORQUESTADOR PRINCIPAL ────────────────────────────────────────
class HadesUnifiedCore:
    def __init__(self):
        self.session = None
        self.abi = HadesABIEngine()
        self.memory = AGI_Memory()

    async def init_session(self):
        connector = aiohttp.TCPConnector(limit=50)
        self.session = aiohttp.ClientSession(connector=connector)

    async def close_session(self):
        if self.session: await self.session.close()

    async def dispatch(self, obj: dict) -> dict:
        action = obj.get("action", "")

        if action == "nucleo_info":
            return {"ncpc": NCPC, "pid": os.getpid(), "estado": "UNIFICADO_ACTIVO"}
        elif action == "atencion":
            return self.memory.attention(obj.get("data", ""))
        elif action == "oraculo":
            return PredictiveOracle.forecast(obj.get("series", [1,2,3,4,5]))
        elif action == "forense":
            path = obj.get("path", str(HOME))
            return self.abi.invoke(0x10, path.encode())
        elif action == "quantum":
            return self.abi.invoke(0x20, b"")
        elif action == "ping":
            return self.abi.invoke(0x01, b"PING")
        elif action == "tensor":
            return self.abi.invoke(0x30, b"")
        elif action == "bash":
            proc = await asyncio.create_subprocess_shell(
                obj["bash"], stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
            return {"comando": obj["bash"], "salida": (stdout or stderr).decode().strip()[:500]}
        elif action == "btc":
            try:
                async with self.session.post(
                    "http://127.0.0.1:8332/",
                    json={"jsonrpc":"1.0","id":"hades","method":obj.get("method","getblockchaininfo"),"params":obj.get("params",[])},
                    auth=aiohttp.BasicAuth("hades","hades_vomega_x90"),
                    timeout=10
                ) as resp:
                    return await resp.json()
            except Exception as e:
                return {"btc_error": str(e)}
        return {"error": "OPCODE_NO_RECONOCIDO"}

    async def procesar_grafo(self, raw_data: dict) -> list:
        tareas = []
        def recolectar(nodo):
            if isinstance(nodo, dict):
                if any(k in nodo for k in ["action","bash","method"]):
                    tareas.append(self.dispatch(nodo))
                for v in nodo.values():
                    if isinstance(v, (dict, list)): recolectar(v)
            elif isinstance(nodo, list):
                for item in nodo: recolectar(item)
        recolectar(raw_data)
        if not tareas:
            return [{"status": "VACIO"}]
        return await asyncio.gather(*tareas, return_exceptions=True)

# ─── INTERFAZ PRINCIPAL ───────────────────────────────────────────
async def ainput(loop):
    return await loop.run_in_executor(None, sys.stdin.readline)

async def main():
    print(f"""
{c(VF,'╔══════════════════════════════════════════════════════════════╗')}
{c(VF,'║')} {c(RC,'HADES vΩ SUPREME - ARQUITECTURA UNIFICADA (5→1 FUSIÓN)')}  {c(VF,'║')}
{c(VF,'║')} {c(CE,'MEMORIA AGI')} {c(MN,'|')} {c(AF,'ORÁCULO')} {c(MN,'|')} {c(AM,'C-ABI (ENTROPÍA+ANNEALING)')} {c(MN,'|')} {c(RC,'BTC-RPC')}  {c(VF,'║')}
{c(VF,'╚══════════════════════════════════════════════════════════════╝')}""")
    print(c(VF, f"> NCPC: {NCPC}"))
    print(c(MN, "> COMANDOS: {\"action\":\"atencion\"|\"oraculo\"|\"forense\"|\"quantum\"|\"ping\"|\"tensor\"|\"bash\"|\"btc\"}"))
    print(c(CE, "> EJEMPLO: {\"action\":\"forense\",\"path\":\"/data/data/com.termux/files/home/HADES_UNIFIED/tmp/hades_in.fifo\"}\n"))

    core = HadesUnifiedCore()
    await core.init_session()
    loop = asyncio.get_running_loop()

    try:
        while True:
            linea = await ainput(loop)
            linea = linea.strip()
            if not linea: continue
            if linea.lower() in ("salir", "exit"): break
            try: data = json.loads(linea)
            except Exception as e:
                print(c(RC, f"> JSON INVÁLIDO: {e}"))
                continue
            t0 = time.perf_counter()
            resultados = await core.procesar_grafo(data)
            t1 = time.perf_counter()
            print(c(VF, f"\n{'='*60}"))
            print(c(AF, f"> {len(resultados)} ACCIÓN(ES) | {round((t1-t0)*1000,2)} ms"))
            for r in resultados:
                if isinstance(r, Exception): print(c(RC, f"> EXCEPCIÓN: {r}"))
                else: print(json.dumps(r, indent=2, ensure_ascii=False))
            print(c(CE, "> ESPERANDO NUEVO VECTOR...\n"))
    except KeyboardInterrupt:
        print(c(RC, "\n[⚡] CERRANDO TÚNELES IPC..."))
    finally:
        await core.close_session()

if __name__ == "__main__":
    asyncio.run(main())

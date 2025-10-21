import socket
import threading
from datetime import datetime

HOST = "localhost"
PORT = 9999
BUFSIZE = 1024
LOG_FILE = "server.txt"

log_lock = threading.Lock()


class LogWriter:
    """Maneja las escrituras seguras en el archivo de log."""

    def __init__(self, filename: str):
        self.file = open(filename, "a", encoding="utf-8")

    def write(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} {message}\n"
        with log_lock:
            self.file.write(log_entry)
            self.file.flush()
        print(log_entry, end="")

    def close(self):
        self.file.close()


def handle_client_connection(conn: socket.socket, addr: tuple, logger: LogWriter):
    logger.write(f"[SERVIDOR] Conectado por {addr}")
    try:
        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            logger.write(f"[LOG RECIBIDO] {data.decode('utf-8')}")
    except ConnectionResetError:
        logger.write(f"[SERVIDOR] Conexión cerrada abruptamente por {addr}")
    finally:
        logger.write(f"[SERVIDOR] Conexión con {addr} cerrada.")
        conn.close()


def start_server():
    logger = LogWriter(LOG_FILE)
    logger.write("[SERVIDOR] Iniciando servidor de logs...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()

            logger.write(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(
                    target=handle_client_connection, args=(conn, addr, logger)
                )
                thread.start()
    finally:
        logger.write("[SERVIDOR] Apagando servidor de logs...")
        logger.close()


if __name__ == "__main__":
    start_server()

import socket
import threading

HOST = "localhost"
PORT = 9999
BUFSIZE = 1024


def handle_client_connection(conn: socket.socket, addr: tuple) -> None:
    print(f"[SERVIDOR] Conectado por {addr}")
    try:
        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            print(f"[LOG RECIBIDO] {data.decode('utf-8')}")
    except ConnectionResetError:
        print(f"[SERVIDOR] Conexión cerrada abruptamente por {addr}")
    finally:
        print(f"[SERVIDOR] Conexión con {addr} cerrada.")
        conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Escuchando en {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(
                target=handle_client_connection, args=(conn, addr)
            )
            thread.start()


if __name__ == "__main__":
    start_server()

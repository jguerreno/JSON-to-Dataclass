import json
import socket
from datetime import datetime
from functools import lru_cache
from typing import Protocol


def log_decorator(func):
    logger: NetworkLogger = __get_network_logger()

    def wrapper(*args, **kwargs):
        logger.log(f"Ejecutando la función '{func.__name__}'")

        try:
            func(*args, **kwargs)
            logger.log(f"Función '{func.__name__}' finalizada.")
        except json.JSONDecodeError as e:
            logger.log(f"ERROR: JSON decoding error. {e}")
        except ValueError as e:
            logger.log(f"ERROR: Invalid input. {e}")
        except Exception as e:
            logger.log(f"ERROR: Unexpected error. {e}")

    return wrapper


class Observer(Protocol):
    def log(self, data: str): ...


class NetworkLogger:
    def __init__(self, host: str = "localhost", port: int = 9999):
        self.host = host
        self.port = port

    def log(self, data: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}]: {data}"

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(log_message.encode("utf-8"))
        except ConnectionRefusedError:
            print(
                f"[NETWORK LOG - ERROR]: No se pudo conectar al servidor de logs en {self.host}:{self.port}"
            )
        except Exception as e:
            print(f"[NETWORK LOG - ERROR]: Ocurrió un error al enviar el log: {e}")


class ConsoleLogger:
    def log(self, data: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[CONSOLE LOG - {timestamp}]: {data}")


class FileLogger:
    def __init__(self, filename="app_log.txt"):
        self.filename = filename

    def log(self, data: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a") as f:
            f.write(f"[{timestamp}]: {data}\n")


@lru_cache
def __get_network_logger() -> NetworkLogger:
    return NetworkLogger()

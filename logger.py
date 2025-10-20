import json
import socket
from datetime import datetime
from functools import wraps
from typing import Protocol


def log_decorator(func):
    """Decorator to log function execution and errors. The class must inherit from Observable."""

    @wraps(func)
    def wrapper(self: Observable, *args, **kwargs):
        self.notify_observers(f"Ejecutando la función '{func.__name__}'")

        try:
            func(self, *args, **kwargs)
            self.notify_observers(f"Función '{func.__name__}' finalizada.")
        except json.JSONDecodeError as e:
            self.notify_observers(f"ERROR: JSON decoding error. {e}")
        except ValueError as e:
            self.notify_observers(f"ERROR: Invalid input. {e}")
        except Exception as e:
            self.notify_observers(f"ERROR: Unexpected error. {e}")

    return wrapper


class Observer(Protocol):
    def log(self, data: str): ...


class Observable:
    def __init__(self):
        self._observers: list[Observer] = []

    def add_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, data: str):
        for observer in self._observers:
            observer.log(data)


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

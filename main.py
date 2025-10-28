import argparse
import multiprocessing
import signal
import sys
import time
import tkinter as tk

from controller import Controller
from log_server import start_server
from logger import ConsoleLogger, FileLogger, NetworkLogger
from model import JsonConverter
from view import View


def run_app():
    json_converter_model = JsonConverter()

    network_logger = NetworkLogger()
    console_logger = ConsoleLogger()
    file_logger = FileLogger()

    root = tk.Tk()
    app_view = View(root)

    app_controller = Controller(json_converter_model, app_view)
    app_controller.add_observer(console_logger)
    app_controller.add_observer(file_logger)
    app_controller.add_observer(network_logger)

    root.mainloop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-server-log",
        dest="with_server_log",
        action="store_true",
        help="Inicia también el servidor de logs",
    )
    args = parser.parse_args()

    stop_event = multiprocessing.Event()
    server_process = None

    def shutdown_handler(signum, frame):
        stop_event.set()
        if server_process and server_process.is_alive():
            server_process.join(timeout=3)
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    if args.with_server_log:
        server_process = multiprocessing.Process(
            target=start_server, args=(stop_event,)
        )
        server_process.start()
        time.sleep(0.5)

    try:
        run_app()
    finally:
        stop_event.set()
        if server_process and server_process.is_alive():
            server_process.join(timeout=3)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()

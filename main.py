import tkinter as tk

from controller import Controller
from logger import ConsoleLogger, FileLogger, NetworkLogger
from model import JsonConverter
from view import View

if __name__ == "__main__":
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

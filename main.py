import tkinter as tk

from controller import Controller
from logger import NetworkLogger
from model import JsonConverter
from view import View

if __name__ == "__main__":
    json_converter_model = JsonConverter()
    network_logger = NetworkLogger()

    root = tk.Tk()
    app_view = View(root)
    app_controller = Controller(json_converter_model, app_view)

    root.mainloop()

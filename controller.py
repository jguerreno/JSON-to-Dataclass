import json

import model
import view
from logger import Observable, log_decorator


class Controller(Observable):
    def __init__(self, model: model.JsonConverter, view: view.View):
        super().__init__()
        self.model = model
        self.view = view
        self.view.set_controller(self)

    @log_decorator
    def handle_conversion(self):
        json_text = self.view.get_json_input()
        if not json_text.strip():
            self.__handle_error("El campo de entrada JSON está vacío.")

        class_name = self.view.get_class_name()

        data = json.loads(json_text)
        if not isinstance(data, dict):
            self.__handle_error("El JSON de entrada debe ser un objeto (diccionario).")

        resultado = self.model.convert(data, class_name)
        self.view.set_dataclass_output(resultado)

    def __handle_error(self, mensaje):
        self.view.set_dataclass_output(f"Error: {mensaje}")
        raise ValueError(mensaje)

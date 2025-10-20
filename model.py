from logger import Observer


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


class JsonConverter:
    def _infer_type(self, valor):
        if isinstance(valor, bool):
            return "bool"
        elif isinstance(valor, int):
            return "int"
        elif isinstance(valor, float):
            return "float"
        elif isinstance(valor, str):
            return "str"
        elif isinstance(valor, list):
            if valor:
                tipo_interno = self._infer_type(valor[0])
                return f"list[{tipo_interno}]"
            return "list"
        return "dict"

    def convert(self, json_input: dict, class_name: str = "ClassName") -> str:
        campos = []
        for clave, valor in json_input.items():
            tipo_dato = self._infer_type(valor)
            campos.append(f"    {clave}: {tipo_dato}")

        resultado_dataclass = (
            f"from dataclasses import dataclass\n\n@dataclass\nclass {class_name}:\n"
        )
        resultado_dataclass += "\n".join(campos)

        return resultado_dataclass

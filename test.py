import unittest

from model import JsonConverter


class TestJsonConverter(unittest.TestCase):
    """
    Pruebas unitarias para la clase JsonConverter del modelo.
    Estas pruebas se centran en la lógica de negocio pura, sin depender
    de la vista o el controlador.
    """

    def setUp(self):
        self.converter = JsonConverter()

    def test_simple_successful_conversion(self):
        json_input = {"nombre": "Ana", "edad": 30, "activo": True}
        expected_output = (
            "from dataclasses import dataclass\n\n"
            "@dataclass\n"
            "class MiDataClass:\n"
            "    nombre: str\n"
            "    edad: int\n"
            "    activo: bool"
        )
        resultado = self.converter.convert(json_input, "MiDataClass")
        self.assertEqual(resultado.strip(), expected_output.strip())

    def test_list_conversion(self):
        json_input = {"id": 1, "tags": ["python", "testing"]}
        expected_output = (
            "@dataclass\nclass ConLista:\n    id: int\n    tags: list[str]"
        )
        resultado = self.converter.convert(json_input, "ConLista")
        self.assertIn(expected_output.strip(), resultado)

    def test_varied_data_types(self):
        json_input = {
            "entero": 10,
            "flotante": 15.5,
            "booleano": False,
            "cadena": "hola",
            "lista_vacia": [],
        }
        resultado = self.converter.convert(json_input, "VariosTipos")
        self.assertIn("entero: int", resultado)
        self.assertIn("flotante: float", resultado)
        self.assertIn("booleano: bool", resultado)
        self.assertIn("cadena: str", resultado)
        self.assertIn("lista_vacia: list", resultado)


if __name__ == "__main__":
    unittest.main()

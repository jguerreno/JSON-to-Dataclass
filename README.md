# Conversor de JSON a Dataclass

Este es un proyecto esta desarrollado en Python con tkinter. La aplicación convierte una cadena de texto en formato JSON a una definición de clase dataclass de Python, infiriendo los tipos de datos de los campos.

El objetivo principal del proyecto es aplicar y demostrar el conocimiento adquirido en el curso Python Avanzado.

## Arquitectura y Patrones de Diseño

### Modelo-Vista-Controlador (MVC)

- Modelo (model.py): Contiene la lógica de negocio pura. La clase JsonConverter se encarga de procesar el json y generar el código de la dataclass. No tiene conocimiento de la interfaz de usuario.
- Vista (view.py): Responsable de toda la interfaz gráfica (GUI) construida con tkinter. Su única función es mostrar los componentes, capturar las entradas del usuario (el JSON y el nombre de la clase) y delegar las acciones al Controlador.
- Controlador (controller.py): Actúa como el intermediario. Escucha los eventos de la Vista (ej. clic en el botón "Convertir"), le pide al Modelo que realice la conversión y, finalmente, toma el resultado del Modelo para actualizar la Vista.

## Patrón Decorador

Se utiliza un decorador para añadir funcionalidad de logging a un método específico sin alterar su código interno.

- `@log_decorator (logger.py)`: Este decorador envuelve al método handle_conversion del controlador. Enviando los logs a un mini servidor de logs

## Estructura de Archivos

```bash
.
├── main.py             # Punto de entrada de la aplicación. Une el MVC.
├── model.py            # Contiene la lógica de negocio (Modelo).
├── view.py             # Contiene la interfaz gráfica (Vista).
├── controller.py       # El intermediario entre el Modelo y la Vista (Controlador).
├── logger.py           # Decorador para logs.
└── log_server.py       # Servidor independiente para recibir logs por la red.
```

## Cómo Ejecutar el Proyecto

Para correr la aplicación, sigue estos pasos.

### Requisitos

`Python 3.x`

No se necesitan librerías externas, ya que el proyecto utiliza únicamente módulos estándar de Python.

### Pasos para la Ejecución

En una terminal se levanta el serivdor de logs:
```bash
python log_server.py
```

Y en la otra se levanta la aplicacion

```bash
python main.py
```

Se abrirá la ventana de la aplicación.

import tkinter as tk
from tkinter import font, scrolledtext


class View:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON a Dataclass Converter")
        self.root.geometry("800x600")

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        self.root.configure(bg="#2E2E2E")
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)
        self.root.option_add("*Font", default_font)

        self.style = {
            "bg": "#2E2E2E",
            "fg": "#FFFFFF",
            "insertbackground": "#FFFFFF",
            "selectbackground": "#555555",
            "font": ("Consolas", 12),
        }

    def _create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.style["bg"], padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_input_frame(main_frame)
        self._create_paned_window(main_frame)
        self._create_convert_button(main_frame)

        # Example JSON placeholder
        self.json_input.insert(
            tk.INSERT,
            '{\n  "id": 1,\n  "nombre": "Producto Ejemplo",\n  "precio": 99.99,\n  "disponible": true,\n  "tags": ["tag1", "tag2"]\n}',
        )

    def _create_input_frame(self, parent):
        input_frame = tk.Frame(parent, bg=self.style["bg"])
        input_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            input_frame,
            text="Nombre de la Clase:",
            bg=self.style["bg"],
            fg=self.style["fg"],
        ).pack(side=tk.LEFT, padx=5)
        self.class_name_entry = tk.Entry(
            input_frame,
            width=30,
            bg="#3C3C3C",
            fg=self.style["fg"],
            insertbackground=self.style["insertbackground"],
        )
        self.class_name_entry.pack(side=tk.LEFT)
        self.class_name_entry.insert(0, "MiDataClass")

    def _create_paned_window(self, parent):
        paned_window = tk.PanedWindow(
            parent, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg=self.style["bg"]
        )
        paned_window.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left panel for JSON input
        left_frame = tk.Frame(paned_window, bg=self.style["bg"])
        tk.Label(
            left_frame, text="Entrada JSON", bg=self.style["bg"], fg=self.style["fg"]
        ).pack(anchor="w")
        self.json_input = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            height=10,
            width=40,
            bg="#3C3C3C",
            fg=self.style["fg"],
            insertbackground=self.style["insertbackground"],
            selectbackground=self.style["selectbackground"],
            font=self.style["font"],
        )
        self.json_input.pack(fill=tk.BOTH, expand=True)
        paned_window.add(left_frame, stretch="always")

        # Right panel for Dataclass output
        right_frame = tk.Frame(paned_window, bg=self.style["bg"])
        tk.Label(
            right_frame,
            text="Salida Dataclass",
            bg=self.style["bg"],
            fg=self.style["fg"],
        ).pack(anchor="w")
        self.dataclass_output = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            height=10,
            width=40,
            bg="#3C3C3C",
            fg=self.style["fg"],
            insertbackground=self.style["insertbackground"],
            selectbackground=self.style["selectbackground"],
            font=self.style["font"],
        )
        self.dataclass_output.pack(fill=tk.BOTH, expand=True)
        paned_window.add(right_frame, stretch="always")

    def _create_convert_button(self, parent):
        self.convert_button = tk.Button(
            parent,
            text="Convertir",
            bg="#007ACC",
            fg="white",
            relief=tk.FLAT,
            activebackground="#005f9e",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.convert_button.pack(pady=10)

    def set_controller(self, controller):
        """Assigns the controller to the button."""
        self.convert_button.config(command=controller.handle_conversion)

    def get_json_input(self):
        return self.json_input.get("1.0", tk.END)

    def get_class_name(self):
        return self.class_name_entry.get() or "ClassName"

    def set_dataclass_output(self, text):
        self.dataclass_output.delete("1.0", tk.END)
        self.dataclass_output.insert(tk.INSERT, text)

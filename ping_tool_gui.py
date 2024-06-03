import tkinter as tk
from tkinter import ttk
from button_handler import ButtonHandler


class PingToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.resizable(True, True)
        self.root.geometry("800x600")
        self.root.title("Ping Tool")
        self.manager = ButtonHandler(self)
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Equipment frame
        equipment_frame = ttk.Frame(main_frame, padding="5")
        equipment_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(equipment_frame, text="Операторские:").grid(
            row=0, column=0, sticky=tk.W
        )
        self.operator_entry = ttk.Entry(equipment_frame)
        self.operator_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(equipment_frame, text="Весы:").grid(row=1, column=0, sticky=tk.W)
        self.weights_entry = ttk.Entry(equipment_frame)
        self.weights_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(equipment_frame, text="Кассы:").grid(row=2, column=0, sticky=tk.W)
        self.cash_entry = ttk.Entry(equipment_frame)
        self.cash_entry.grid(row=2, column=1, padx=5, pady=2)

        # Buttons frame
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        button_frame.columnconfigure([0, 1, 2], weight=1)

        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            padding=10,
            width=18,
        )

        self.ping_sm_button = ttk.Button(
            button_frame,
            text="Ping SM",
            style="Custom.TButton",
            command=self.manager.ping_sm_range,
        )
        self.ping_sm_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            style="Custom.TButton",
            command=self.manager.stop_ping,
        )
        self.stop_button.grid(row=0, column=1, padx=5)

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            style="Custom.TButton",
            command=self.manager.clear_results,
        )
        self.clear_button.grid(row=0, column=2, padx=5)

        # Result text with scrollbar
        result_frame = ttk.Frame(main_frame, padding="5")
        result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(2, weight=1)

        self.result_text = tk.Text(result_frame, height=26, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(
            result_frame, orient=tk.VERTICAL, command=self.result_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text["yscrollcommand"] = scrollbar.set

import tkinter as tk
from tkinter import ttk
from ping_manager import PingManager

class PingToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Tool")
        self.manager = PingManager(self)
        self.create_widgets()
    
    def create_widgets(self):

        # Labels
        tk.Label(self.root, text="Операторские ПК:").pack()
        self.operator_entry = tk.Entry(self.root)
        self.operator_entry.pack()

        tk.Label(self.root, text="Весы:").pack()
        self.weights_entry = tk.Entry(self.root)
        self.weights_entry.pack()

        tk.Label(self.root, text="Кассы:").pack()
        self.cash_entry = tk.Entry(self.root)
        self.cash_entry.pack()

        tk.Label(self.root, text="").pack()

        # Buttons
        style = ttk.Style()
        style.configure("Custom.TButton", foreground="black", background="lightgray", padding=10, width=18)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        self.ping_sm_button = ttk.Button(button_frame, text="Ping SM", style="Custom.TButton", command=self.manager.ping_sm)
        self.ping_sm_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", style="Custom.TButton", command=self.manager.stop_ping)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear",  style="Custom.TButton", command=self.manager.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.result_text = tk.Text(self.root, height=26, width=80)
        self.result_text.pack()
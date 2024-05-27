import threading
import tkinter as tk
from ping_handler import PingHandler


class ButtonHandler:
    def __init__(self, gui):
        self.ph = PingHandler(self)
        self.gui = gui
        self.stop_flag = True

    def update_results(self, result, color=None):
        self.gui.result_text.config(state=tk.NORMAL)
        if color:
            self.gui.result_text.tag_configure(color, foreground=color)
            self.gui.result_text.insert(tk.END, result + "\n", color)
        else:
            self.gui.result_text.insert(tk.END, result + "\n")
        self.gui.result_text.see(tk.END)
        self.gui.result_text.config(state=tk.DISABLED)
        self.gui.root.after(100, self.gui.result_text.update_idletasks)

    def ping_sm_range(self):
        def get_entry_value(entry):
            return int(entry.get()) if entry.get() else 0

        if self.stop_flag:
            self.stop_flag = False
            operator_value = get_entry_value(self.gui.operator_entry)
            weights_value = get_entry_value(self.gui.weights_entry)
            cash_value = get_entry_value(self.gui.cash_entry)
            threading.Thread(
                target=self.ph.ping_sm_range,
                args=(
                    operator_value,
                    weights_value,
                    cash_value,
                ),
            ).start()

    def stop_ping(self):
        if not self.stop_flag:
            self.update_results("Aborted\n")
        self.stop_flag = True

    def clear_results(self):
        self.gui.result_text.config(state=tk.NORMAL)
        self.gui.result_text.delete(1.0, tk.END)
        self.gui.result_text.config(state=tk.DISABLED)

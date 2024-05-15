import ping3
import threading
import wmi
import tkinter as tk
import ping_handler as PingHandler

class PingManager:
    def __init__(self, gui):
        self.ping_handler = PingHandler(self)
        self.gui = gui
        self.stop_flag = True
        self.running_flag = False

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

    def get_entry_value(entry):
    return int(entry.get()) if entry.get() else 0

    def ping_sm(self):
        if not self.running_flag:
            self.running_flag = True
            self.stop_flag = False
            operator_value = get_entry_value(self.gui.operator_entry)
            weights_value = get_entry_value(self.gui.weights_entry)
            cash_value = get_entry_value(self.gui.cash_entry)
            ip_list = self.form_ip_list(
                operator_value,
                weights_value,
                cash_value,
            )
            threading.Thread(
                target=self.ping_all_ip,
                args=(ip_list,),
            ).start()

    def stop_ping(self):
        if not self.stop_flag:
            self.running_flag = False
            self.update_results("Aborted\n")
        self.stop_flag = True

    def clear_results(self):
        self.gui.result_text.config(state=tk.NORMAL)
        self.gui.result_text.delete(1.0, tk.END)
        self.gui.result_text.config(state=tk.DISABLED)
import ping3
import threading
import wmi
import tkinter as tk

# if kassa > 10, ip_range(141, 160)


class PingManager:
    def __init__(self, gui):
        self.gui = gui
        self.stop_flag = True
        self.running_flag = False
        self.ip = self.get_ip("Realtek PCIe GbE Family Controller")
        # self.ip = self.get_ip("Kerio")
        self.subnet = self.get_subnet(self.ip)
        # self.solo_kiosk_range = [1, 2, 41, 101]
        # self.operator = range(1, 11)
        # self.weights = range(11, 21)
        # self.cash = range(21, 41)
        # self.terminal = range(41, 61)
        # self.fiscal = range(101, 121)
        # self.sm_range = (
        #     list(self.operator)
        #     + list(self.weights)
        #     + list(self.cash)
        #     + list(self.terminal)
        #     + list(self.fiscal)
        # )
        # print(self.subnet)

    def get_ip(self, interface_description_contains):
        try:
            c = wmi.WMI()
            for iface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                if interface_description_contains in iface.Description:
                    for ip in iface.IPAddress:
                        if ":" not in ip:
                            return ip
        except Exception as e:
            print(f"Failed to get IPv4 address: {e}")
        return None

    def get_subnet(self, ip):
        ip_split = ip.split('.')
        subnet = ip_split[2]
        return subnet

    def ping_all_ip(self, ip_list):
        print(ip_list)
        not_reached_ips = []
        for ip in ip_list:
            if self.stop_flag:
                break
            rtt = ping3.ping(ip)
            if rtt is not None:
                rtt_formatted = "{:.0f}".format(rtt * 1000)
                result = f"{ip} was reached in {rtt_formatted} ms"
                color = "green"
            else:
                result = f"{ip} was not reached"
                color = "red"
                not_reached_ips.append(ip)
            self.update_results(result, color)
        if not self.stop_flag:
            self.update_results("Completed")
            self.running_flag = False
            self.stop_flag = True

    def form_ip_list(self, operator=0, weights=0, cash=0):
        ip_list = []
        if operator:
            for i in range(1, operator + 1):
                ip_list.append(f"192.168.{self.subnet}.{i}")
        if weights:
            for i in range(1, weights + 1):
                ip_list.append(f"192.168.{self.subnet}.{i + 10}")
        if cash:
            for i in range(1, cash + 1):
                ip_list.append(f"192.168.{self.subnet}.{i + 20}")
                ip_list.append(f"192.168.{self.subnet}.{i + 40}")
                ip_list.append(f"192.168.{self.subnet}.{i + 100}")
        return ip_list

    # def set_color(self, result):
    #     color = ""
    #     match result:
    #         case "Aborted":
    #             color = "red"
    #         case "Completed":
    #             color = "green"
    #         case _:
    #             color = None
    #     return color

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

    def get_operator_value(self):
        return int(self.gui.operator_entry.get()) if self.gui.operator_entry.get() else 0

    def get_weights_value(self):
        return int(self.gui.weights_entry.get()) if self.gui.weights_entry.get() else 0

    def get_cash_value(self):
        return int(self.gui.cash_entry.get()) if self.gui.cash_entry.get() else 0

    def ping_sm(self):
        if not self.running_flag:
            self.running_flag = True
            self.stop_flag = False
            operator_value = self.get_operator_value()
            weights_value = self.get_weights_value()
            cash_value = self.get_cash_value()
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
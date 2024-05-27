import ping3
from equipment_manager import EquipmentManager


class PingHandler:
    def __init__(self, button_handler):
        self.bh = button_handler
        self.equip = EquipmentManager()
        self.general_ip_list = set()
    #     self.equipment_types = {
    #         'operator': {0: "Операторский"},
    #         'weights': {10: "Весы"},
    #         'cash': {20: "Касса"},
    #         'terminal': {40: "Терминал"},
    #         'terminal_long': {140: "Терминал"},
    #         'exelio': {100: "Кассовый аппарат"}
    #     }
    #     self.known_adapters = ["Realtek PCIe GbE Family Controller", "Gigabit"]
    #     self.known_adapters = ["Kerio"]
    #     self.ip = self.get_ip_from_adapter(self.known_adapters)
    #     self.subnet = self.get_subnet(self.ip)

    # def get_ip_from_adapter(self, interface_description_contains):
    #     try:
    #         c = wmi.WMI()
    #         for iface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
    #             for i in interface_description_contains:
    #                 if i and i in iface.Description:
    #                     for ip in iface.IPAddress:
    #                         if ":" not in ip:
    #                             return ip
    #     except Exception as e:
    #         print(f"Failed to get IPv4 address: {e}")
    #     return None

    # def get_subnet(self, ip):
    #     ip_split = ip.split(".")
    #     subnet = ip_split[2]
    #     return subnet

    def ping_all_ip(self, ip_list, equipment_type):
        ip_counter = 0
        for ip in ip_list:
            ip_counter += 1
            if self.bh.stop_flag:
                break
            rtt = ping3.ping(ip, timeout=1)
            if rtt is not None:
                rtt_formatted = "{:.0f}".format(rtt * 1000)
                result = f"{equipment_type} {ip_counter}({ip}) was reached in {rtt_formatted} ms"
                color = "green"
            else:
                result = f"{equipment_type} {ip_counter}({ip}) was not reached"
                color = "red"
                self.not_reached_ip.append(f"{ip}")
            self.bh.update_results(result, color)

    def print_not_reached(self, not_reached_ip):
        if not_reached_ip:
            self.bh.update_results("Нет ответа от:")
            for ip in not_reached_ip:
                self.bh.update_results(f"=({ip})", "red")

    def ping_sm_range(self, operator=0, weights=0, cash=0):
        self.not_reached_ip = []
        # Make a list instead?
        self.equip.set_equipment_value('operator', operator) # ???
        self.equip.set_equipment_value(weights)
        self.equip.set_equipment_value(cash)
        

        def form_ip_list(count, offset):
            equipment_list = []
            for i in range(1, count + 1):
                equipment_list.append(f"192.168.{self.subnet}.{i + offset}")
            return equipment_list

        def execute_ping_list(equipment_type, offset, equipment_name):
            self.bh.update_results(f"{equipment_name}:")
            equipment_list = form_ip_list(equipment_type, offset)
            self.general_ip_list.update(equipment_list)
            self.ping_all_ip(equipment_list, equipment_name)
            self.bh.update_results("\n")

        def ip_key(ip):
            return tuple(map(int, ip.split(".")))

        def equipment_ping():
                    # if weights and not self.bh.stop_flag:
                    #     execute_ping_list(weights, self.equipment_types_keys[1], "Весы", "Весы")
                    # if cash and not self.bh.stop_flag:
                    #     execute_ping_list(cash, self.equipment_types_keys[2], "Касса", "Кассы")
                    #     if not self.bh.stop_flag:
                    #         if cash < 10:
                    #             execute_ping_list(
                    #                 cash, self.equipment_types_keys[3], "Терминал", "Терминалы"
                    #             )
                    #         else:
                    #             execute_ping_list(
                    #                 cash, self.equipment_types_keys[4], "Терминал", "Терминалы"
                    #             )
                    #     if not self.bh.stop_flag:
                    #         execute_ping_list(
                    #             cash,
                    #             self.equipment_types_keys[5],
                    #             "Кассовый аппарат",
                    #             "Кассовые аппараты",
                    #         )

            if self.not_reached_ip and not self.bh.stop_flag:
                self.print_not_reached(sorted(self.not_reached_ip, key=ip_key))

        equipment_ping()

        self.bh.update_results("\n")

        self.bh.stop_flag = True

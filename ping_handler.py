import ping3
from equipment_manager import EquipmentManager


class PingHandler:
    def __init__(self, button_handler):
        self.bh = button_handler
        self.equip = EquipmentManager()
        self.not_reached_ip = set()
        self.general_ip_list = set()

    def update_equipment_values(self, operator, weights, cash):
        self.equip.set_equipment_value('operator', operator)
        self.equip.set_equipment_value('weights', weights)
        self.equip.set_equipment_value('cash', cash)

    def ping_all_ip(self, ip_list, key):
        name = self.equip.equipment[key]['name']
        ip_counter = 0
        for ip in ip_list:
            ip_counter += 1
            if self.bh.stop_flag:
                self.update_results("Stopped")
                break
            self.ping_ip(ip, name, ip_counter)

    def ping_ip(self, ip, name, ip_counter):
        rtt = ping3.ping(ip, timeout=1)
        if rtt is not None:
            rtt_formatted = "{:.0f}".format(rtt * 1000)
            result = f"{name} {ip_counter}({ip}): was reached in {rtt_formatted} ms"
            color = "green"
        else:
            result = f"{name} {ip_counter}({ip}): was not reached"
            color = "red"
            self.not_reached_ip.add(ip)
        self.bh.update_results(result, color)

    def print_not_reached(self):
        not_reached = self.not_reached_ip
        if sorted(not_reached, key=lambda x: int(x)):
            self.bh.update_results("Нет ответа от:")
            for ip in not_reached:
                self.bh.update_results(ip, "red")

    def ping_sm(self):
        for key in self.equip.equipment.keys():
            self.bh.update_results(f"{self.equip.equipment[key]['name']}:")
            equipment_list = self.form_ip_list(key)
            self.general_ip_list.update(equipment_list)
            self.ping_all_ip(equipment_list, key)
            self.bh.update_results("\n")
        self.print_not_reached()
        self.bh.stop_flag = True

    def form_ip_list(self, equipment, count_from=1, count_to=1):
        equipment_list = []
        max_value = self.equip.equipment[equipment]['value']
        if count_to > 1 and count_to <= max_value:
            for i in range(count_from, count_to + 1):
                equipment_list.append(f"192.168.{self.equip.subnet}.{i + self.equip.equipment[equipment]['offset']}")
        elif count_to > max_value:
            self.bh.update_results("Out of range")
        else:
            for i in range(count_from, max_value + 1):
                equipment_list.append(f"192.168.{self.equip.subnet}.{i + self.equip.equipment[equipment]['offset']}")
        return equipment_list

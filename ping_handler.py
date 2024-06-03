import ping3
from equipment_manager import EquipmentManager
import concurrent.futures


class PingHandler:
    def __init__(self, button_handler):
        self.bh = button_handler
        self.equip = EquipmentManager()
        self.not_reached_ip = set()
        self.general_ip_list = set()

    def update_equipment_values(self, operator, weights, cash):
        self.equip.set_equipment_value("operator", operator)
        self.equip.set_equipment_value("weights", weights)
        self.equip.set_equipment_value("cash", cash)

    def ping_all_ip(self, ip_list, key):
        name = self.equip.equipment[key]["name"]
        count = 0
        for ip in ip_list:
            count += 1
            if self.bh.stop_flag:
                self.update_results("Остановлено")
                break
            self.ping_ip(ip, name, count)

    def ping_ip(self, ip, name, count):
        rtt = ping3.ping(ip, timeout=1)
        if rtt is not None:
            rtt_formatted = "{:.0f}".format(rtt * 1000)
            result = f"{name} {count} ({ip}): ответ за {rtt_formatted} мс"
            color = "green"
        else:
            result = f"{name} {count} ({ip}): нет ответа"
            color = "red"
            self.not_reached_ip.add(ip)
        self.general_ip_list.add(ip)
        self.bh.update_results(result, color)

    def print_not_reached(self):
        not_reached = self.not_reached_ip
        if not_reached:
            self.bh.update_results("Нет ответа от:")
            for ip in sorted(not_reached, key=self.sort_ip):
                self.bh.update_results(f"{ip}", "red")

    def print_availability(self):
        all_ip_num = len(self.general_ip_list)
        available_num = all_ip_num - len(self.not_reached_ip)
        self.bh.update_results(
            f"{len(self.not_reached_ip)} из {len(self.general_ip_list)} устройств недоступны.\n"
        )

    def sort_ip(self, ip):
        parts = ip.split(".")
        return [int(part) for part in parts]

    def ping_sm(self):
        for key in self.equip.equipment.keys():
            self.bh.update_results(f"{self.equip.equipment[key]['name']}:")
            equipment_list = self.form_ip_list(key)
            self.general_ip_list.update(equipment_list)
            self.ping_all_ip(equipment_list, key)
            self.bh.update_results("\n")
        self.print_availability()
        self.print_not_reached()

        self.bh.stop_flag = True

    def form_ip_list(self, equipment, count_from=1, count_to=1):
        equipment_data = self.equip.equipment[equipment]
        equipment_list = []
        max_value = equipment_data["value"]

        if count_to > 1 and count_to <= max_value:
            range_to_use = range(count_from, count_to + 1)
        elif count_to > max_value:
            self.bh.update_results("Out of range")
            return []
        else:
            range_to_use = range(count_from, max_value + 1)

        subnet = self.equip.subnet
        offset = equipment_data["offset"]
        for i in range_to_use:
            equipment_list.append(f"192.168.{subnet}.{i + offset}")

        return equipment_list

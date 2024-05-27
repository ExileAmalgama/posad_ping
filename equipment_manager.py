import wmi

class EquipmentManager:
    def __init__(self):
        self.equipment_list = {
            'operator': {offset: 0, name: "Операторский", value: 0},
            'weights': {offset: 10, name: "Весы", value: 0},
            'cash': {offset: 20, name: "Касса", value: 0},
            'terminal': {offset: 40, name: "Терминал", value: 0},
            'terminal_long': {offset: 140, name: "Терминал", value: 0},
            'exelio': {offset: 100, name: "Кассовый аппарат", value: 0}
        }
        self.known_adapters = ["Realtek PCIe GbE Family Controller", "Gigabit"]
        self.known_adapters = ["Kerio"]
        self.equipment_offset_list = get_equipment_offsets()
        self.equipment_name_list = get_equipment_names()
        self.equipment_value_list = get_equipment_values()
        self.ip = self.get_ip_from_adapter(self.known_adapters)
        self.subnet = self.get_subnet(self.ip)
    
    def set_equipment_value(self, equip_type, value):
        if equip_type == 'cash':
            self.equipment_list[equip_type]['value'] = value
            if value < 10:
                # del self.equipment_list['terminal_long']
                self.equipment_list['terminal']['value'] = value
            else:
                # del self.equipment_list['terminal']
                self.equipment_list['terminal_long']['value'] = value
            self.equipment_list['exelio']['value'] = value
        else:    
            self.equipment_list[equip_type]['value'] = value

    def get_equipment_offsets(self):
        return [item['offset'] for item in self.equipment_list.values()]

    def get_equipment_names(self):
        return [item['name'] for item in self.equipment_list.values()]

    def get_equipment_values(self):
        return [item['value'] for item in self.equipment_list.values()]

    def get_ip_from_adapter(self, interface_description_contains):
        try:
            c = wmi.WMI()
            for iface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                for i in interface_description_contains:
                    if i and i in iface.Description:
                        for ip in iface.IPAddress:
                            if ":" not in ip:
                                return ip
        except Exception as e:
            print(f"Failed to get IPv4 address: {e}")
        return None

    def get_subnet(self, ip):
        ip_split = ip.split(".")
        subnet = ip_split[2]
        return subnet
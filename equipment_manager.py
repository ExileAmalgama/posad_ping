import wmi

class EquipmentManager:
    def __init__(self):
        self.equipment = {
            'operator': {'offset': 0, 'name': "Операторские", 'value': 0},
            'weights': {'offset': 10, 'name': "Весы", 'value': 0},
            'cash': {'offset': 20, 'name': "Кассы", 'value': 0},
            'terminal': {'offset': 40, 'name': "Терминалы", 'value': 0},
            'exelio': {'offset': 100, 'name': "Кассовые аппараты", 'value': 0}
        }
        self.known_adapters = ["Realtek PCIe GbE Family Controller", "Gigabit"]
        self.known_adapters = ["Kerio"]
        self.ip = self.get_ip_from_adapter(self.known_adapters)
        self.subnet = self.get_subnet(self.ip)
    
    def set_equipment_value(self, equip_type, value):
        if equip_type == 'cash':
            self.equipment[equip_type]['value'] = value
            self.equipment['terminal']['value'] = value
            if value < 10:
                self.equipment['terminal']['offset'] = 40
            else:
                self.equipment['terminal']['offset'] = 140
            self.equipment['exelio']['value'] = value
        else:    
            self.equipment[equip_type]['value'] = value

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
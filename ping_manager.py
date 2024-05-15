import ping3

class PingHandler:
    def __init__(self):
        self.ip_list = []
        self.known_adapters = ["Realtek PCIe GbE Family Controller", "Gigabit"]
        self.known_adapters = ["Kerio"]
        self.ip = self.get_ip_from_adapter(self.known_adapters)
        self.subnet = self.get_subnet(self.ip)

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
        ip_split = ip.split('.')
        subnet = ip_split[2]
        return subnet

    def ping_all_ip(self, ip_list):
        not_reached_ips = []
        for ip in ip_list:
            if self.stop_flag:
                break
            rtt = ping3.ping(ip, timeout=1)
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

        def append_ip_list(count, offset, additional_ips=None):
            equipment_ip_list = []
            for i in range(1, count + 1):
                ip_list.append(f"192.168.{self.subnet}.{i + offset}")
                if additional_ips:
                    for additional_offset in additional_ips:
                        equipment_ip_list.append(f"192.168.{self.subnet}.{i + additional_offset}")
            return equipment_ip_list

        def execute_ping_list(ip_list, offset, equipment_type):
            self.update_results(f"{equipment_type}:")
            equipment_list = append_ip_list(ip_list, offset)
            self.ping_all_ip(equipment_list)
            self.update_results("\n")
        
        if operator:
            append_ip_list(operator, 0, "Операторские")        
        if weights:
            append_ip_list(weights, 10, "Весы")        
        if cash:
            append_ip_list(weights, 10, "Кассы")
        
        return ip_list
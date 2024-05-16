import ping3
import wmi


class PingHandler:
    def __init__(self, button_handler):
        self.bh = button_handler
        self.general_ip_list = set()
        self.not_reached_ips = set()
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
        ip_split = ip.split(".")
        subnet = ip_split[2]
        return subnet

    def ping_all_ip(self, ip_list):
        for ip in ip_list:
            if self.bh.stop_flag:
                break
            rtt = ping3.ping(ip, timeout=1)
            if rtt is not None:
                rtt_formatted = "{:.0f}".format(rtt * 1000)
                result = f"{ip} was reached in {rtt_formatted} ms"
                color = "green"
            else:
                result = f"{ip} was not reached"
                color = "red"
                self.not_reached_ips.add(ip)
            self.bh.update_results(result, color)

    def ping_sm_range(self, operator=0, weights=0, cash=0):
        def form_ip_list(count, offset):
            equipment_list = []
            for i in range(1, count + 1):
                equipment_list.append(f"192.168.{self.subnet}.{i + offset}")
            return equipment_list

        def execute_ping_list(ip_list, offset, equipment_type=""):
            if equipment_type:
                self.bh.update_results(f"{equipment_type}:")
            equipment_list = form_ip_list(ip_list, offset)
            self.general_ip_list.update(equipment_list)
            self.ping_all_ip(equipment_list)
            if equipment_type:
                self.bh.update_results("\n")

        if operator and self.bh.running_flag:
            execute_ping_list(operator, 0, "Операторские")
        if weights and self.bh.running_flag:
            execute_ping_list(weights, 10, "Весы")
        if cash and self.bh.running_flag:
            execute_ping_list(cash, 20, "Кассы")
            if self.bh.running_flag:
                if cash < 10:
                    execute_ping_list(cash, 40, "Терминалы")
                else:
                    execute_ping_list(cash, 140, "Терминалы")
            if self.bh.running_flag:
                execute_ping_list(cash, 100, "Кассовые аппараты")

        if self.not_reached_ips and self.bh.running_flag:
            self.bh.print_not_reached(self.not_reached_ips)

        if not self.bh.stop_flag:
            self.bh.running_flag = False
            self.bh.stop_flag = True

from OSILayer import OSILayer
from DataLinkLayer import DataLinkLayer

class NetworkLayer(OSILayer):
    def __init__(self, ip_address, routing_table, next_layer=None):
        # ip_address: Simulated IP address of this node.
        # routing_table: A dictionary mapping destination IPs to next-hop MAC addresses.
        
        super().__init__(next_layer)
        self.ip_address = ip_address
        self.routing_table = routing_table  # { "192.168.1.2": "AA:BB:CC:DD:EE:02" }

    def send(self, data, dest_ip):
        # Encapsulates data into a 'packet' and sends it to the next layer.

        if dest_ip not in self.routing_table:
            print(f"Network Layer: No route to {dest_ip}. Dropping packet.")
            return

        dest_mac = self.routing_table[dest_ip]  # Get MAC address for next hop
        packet = f"{self.ip_address}>{dest_ip}|{data}|PACKET_END"
        print(f"Network Layer: Sending packet -> {packet} via MAC {dest_mac}")

        if self.next_layer:
            self.next_layer.send(packet, dest_mac)  # Pass packet down to Data Link Layer

    def receive(self, packet):
        # Processes received packet and extracts data if the destination matches.
        try:
            ip_header, data, _ = packet.split('|')
            src_ip, dest_ip = ip_header.split('>')

            print(f"Network Layer: Received packet from {src_ip} to {dest_ip}")

            if dest_ip != self.ip_address:
                print("Network Layer: Packet not for this device. Dropping.")
                return

            print(f"Network Layer: Data extracted -> {data}")

            if self.next_layer:
                self.next_layer.receive(data)  # Pass to the next layer (Transport Layer)

        except ValueError:
            print("Network Layer: Packet format error")

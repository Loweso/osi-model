import socket
from OSILayer import OSILayer

class PhysicalLayer(OSILayer):
    def __init__(self, role, host='localhost', port=12345, next_layer=None):
        super().__init__(next_layer)
        self.role = role  # "client" or "server"
        self.host = host
        self.port = port

        if self.role == "server":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)  # Listen for one connection
            print(f"Physical Layer Server listening on {self.host}:{self.port}")

    def send(self, data):
        """Simulates sending data as raw bits (client mode)."""
        if self.role != "client":
            raise ValueError("send() should only be called on a client instance")

        bits = ''.join(format(ord(char), '08b') for char in data)  # Convert to binary
        print(f"Physical Layer (Client): Sending bits -> {bits}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(bits.encode())

    def receive(self):
    # Simulates receiving data in binary (server mode).
        if self.role != "server":
            raise ValueError("receive() should only be called on a server instance")

        while True:  # Keep the server running to handle multiple messages
            conn, _ = self.server_socket.accept()
            with conn:
                binary_data = conn.recv(1024).decode()

            text_data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))  # Convert back to text
            print(f"Physical Layer (Server): Received bits -> {binary_data}")
            print(f"Physical Layer (Server): Decoded text -> {text_data}")

            if self.next_layer:
                self.next_layer.receive(text_data)  # Pass up the OSI stack


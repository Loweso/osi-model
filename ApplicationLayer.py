from OSILayer import OSILayer

class ApplicationLayer(OSILayer):
    def __init__(self, role, next_layer=None):
        """
        Application layer simulating HTTP-like requests & responses.
        :param role: "client" or "server"
        """
        super().__init__(next_layer)
        self.role = role

    def send_request(self, method, resource, dest_ip="192.168.1.1"):
        """Simulates an HTTP-like request (for clients)."""
        if self.role != "client":
            raise ValueError("send_request() should only be called by a client")

        request = f"{method} {resource} HTTP/1.1"
        print(f"Application Layer (Client): Sending request -> {request}")

        if self.next_layer:
            self.next_layer.send(request, dest_ip)  # Now correctly passing dest_ip

    def send_response(self, status_code, message):
        """Simulates an HTTP-like response (for servers)."""
        if self.role != "server":
            raise ValueError("send_response() should only be called by a server")

        response = f"HTTP/1.1 {status_code} {message}"
        print(f"Application Layer (Server): Sending response -> {response}")

        if self.next_layer:
            self.next_layer.send(response)  # Pass to Presentation Layer

    def receive(self, data):
        """Processes received HTTP-like requests & responses."""
        print(f"Application Layer: Received -> {data}")

        if self.role == "server" and data.startswith("GET"):
            # Simulate processing a GET request
            resource = data.split()[1]  # Extract resource (e.g., "/hello")
            response_message = f"Hello, you requested {resource}"
            self.send_response("200 OK", response_message)

        elif self.role == "client" and data.startswith("HTTP/1.1"):
            # Client received a response
            print(f"Application Layer (Client): Server Response -> {data}")

        # Pass up if there's another layer (e.g., an application handler)
        if self.next_layer:
            self.next_layer.receive(data)

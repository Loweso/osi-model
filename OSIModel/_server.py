from PhysicalLayer import PhysicalLayer

if __name__ == "__main__":
    server_physical = PhysicalLayer(role="server")  # Server mode
    server_physical.receive()  # Keep server running

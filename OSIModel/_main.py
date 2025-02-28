import time
from PhysicalLayer import PhysicalLayer
from DataLinkLayer import DataLinkLayer
from NetworkLayer import NetworkLayer
from SessionLayer import SessionLayer
from PresentationLayer import PresentationLayer
from ApplicationLayer import ApplicationLayer

if __name__ == "__main__":
    physical = PhysicalLayer(role="client")
    datalink = DataLinkLayer(mac_address="AA:BB:CC:DD:EE:02", next_layer=physical)

    routing_table = {"192.168.1.1": "AA:BB:CC:DD:EE:01"} 
    network = NetworkLayer(ip_address="192.168.1.2", routing_table=routing_table, next_layer=datalink)

    session = SessionLayer(session_id="12345", next_layer=network)
    presentation = PresentationLayer(encryption_key="secure123", next_layer=session)

    application = ApplicationLayer(role="client", next_layer=presentation)

    time.sleep(1)

    # Simulating an HTTP-like request from client
    application.send_request("GET", "/hello")

    time.sleep(1)

    # Closing session
    session.close_session(dest_ip="192.168.1.1")

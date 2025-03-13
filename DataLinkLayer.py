from OSILayer import OSILayer

class DataLinkLayer(OSILayer):
    def __init__(self, mac_address, next_layer=None):
        # "mac_address" is the string representing this node's MAC address.
        super().__init__(next_layer)
        self.mac_address = mac_address

    def send(self, data, dest_mac):
        # Frames the data with MAC header and trailer and then passes it

        # To onstruct a simple frame:
        # Frame format: "MAC_START|SRC:<source>|DST:<destination>|DATA:<payload>|MAC_END"
        frame = f"MAC_START|SRC:{self.mac_address}|DST:{dest_mac}|DATA:{data}|MAC_END"
        print(f"Data Link Layer: Framed data for transmission: {frame}")

        # Send the frame down to the Physical Layer.
        if self.next_layer:
            self.next_layer.send(frame)

    def receive(self, frame):
        # Receives a frame, validates it, extracts the payload,
        # and passes it up the OSI stack.
        
        print(f"Data Link Layer: Received frame: {frame}")

        # Check that the frame starts and ends with the expected markers.
        if not (frame.startswith("MAC_START") and frame.endswith("MAC_END")):
            print("Data Link Layer: Invalid frame format")
            return

        # Remove the frame markers
        frame_content = frame[len("MAC_START|") : -len("|MAC_END")]

        # Parse the frame components.
        components = {}
        for part in frame_content.split('|'):
            if ':' in part:
                key, value = part.split(":", 1)
                components[key] = value

        # Validate that the destination MAC address matches this node's address.
        if components.get("DST") != self.mac_address:
            print("Data Link Layer: Frame not addressed to this MAC. Dropping frame.")
            return

        # Extract the actual data payload.
        payload = components.get("DATA", "")
        print(f"Data Link Layer: Extracted payload: {payload}")

        # Pass the payload up the OSI stack (if there's another layer above).
        if self.next_layer:
            self.next_layer.receive(payload)

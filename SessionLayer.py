from OSILayer import OSILayer

class SessionLayer(OSILayer):
    def __init__(self, session_id, next_layer=None):
        super().__init__(next_layer)
        self.session_id = session_id
        self.active_sessions = set()

    def send(self, data, dest_ip):
        """Ensures a session exists before sending data."""
        if self.session_id not in self.active_sessions:
            print(f"Session Layer: Establishing session with {dest_ip}...")
            self.active_sessions.add(self.session_id)
            handshake_message = f"SESSION_START|{self.session_id}"
            if self.next_layer:
                self.next_layer.send(handshake_message, dest_ip)

        session_data = f"SESSION_DATA|{self.session_id}|{data}"
        print(f"Session Layer: Sending data within session {self.session_id}")
        if self.next_layer:
            self.next_layer.send(session_data, dest_ip)

    def receive(self, packet):
        """Handles session establishment and data transmission."""
        if packet.startswith("SESSION_START"):
            _, session_id = packet.split("|", 1)
            print(f"Session Layer: Session {session_id} established.")
            self.active_sessions.add(session_id)

        elif packet.startswith("SESSION_DATA"):
            _, session_id, data = packet.split("|", 2)
            if session_id in self.active_sessions:
                print(f"Session Layer: Received session data for session {session_id}")
                if self.next_layer:
                    self.next_layer.receive(data)
            else:
                print("Session Layer: Data received for an unknown session. Dropping.")

        elif packet.startswith("SESSION_CLOSE"):
            _, session_id = packet.split("|", 1)
            print(f"Session Layer: Closing session {session_id}.")
            self.active_sessions.discard(session_id)

    def close_session(self, dest_ip):
        """Sends a session termination request."""
        if self.session_id in self.active_sessions:
            print(f"Session Layer: Closing session {self.session_id} with {dest_ip}")
            self.active_sessions.remove(self.session_id)
            session_close_msg = f"SESSION_CLOSE|{self.session_id}"
            if self.next_layer:
                self.next_layer.send(session_close_msg, dest_ip)

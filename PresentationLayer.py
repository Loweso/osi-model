from OSILayer import OSILayer
import zlib

class PresentationLayer(OSILayer):
    def __init__(self, encryption_key="default_key", next_layer=None):
        super().__init__(next_layer)
        self.encryption_key = encryption_key  # Used for XOR encryption

    def encrypt(self, data):
        """Custom XOR encryption without external libraries."""
        key_bytes = self.encryption_key.encode()
        data_bytes = data.encode()
        encrypted_bytes = bytes([data_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data_bytes))])
        return encrypted_bytes.hex()  # Convert bytes to hex for safe transmission

    def decrypt(self, encrypted_data):
        """Custom XOR decryption without external libraries."""
        key_bytes = self.encryption_key.encode()
        encrypted_bytes = bytes.fromhex(encrypted_data)  # Convert hex back to bytes
        decrypted_bytes = bytes([encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes))])
        return decrypted_bytes.decode()

    def compress(self, data):
        """Compress data using zlib and return as hex string."""
        return zlib.compress(data.encode()).hex()

    def decompress(self, compressed_data):
        """Decompress data using zlib from hex string."""
        return zlib.decompress(bytes.fromhex(compressed_data)).decode()

    def send(self, data, dest_ip):
        """Encrypts, compresses, and sends data to the next layer."""
        compressed_data = self.compress(data)
        encrypted_data = self.encrypt(compressed_data)
        print(f"Presentation Layer: Sending encrypted & compressed data -> {encrypted_data}")

        if self.next_layer:
            self.next_layer.send(encrypted_data, dest_ip)

    def receive(self, data):
        """Decrypts, decompresses, and passes data up."""
        try:
            decrypted_data = self.decrypt(data)
            decompressed_data = self.decompress(decrypted_data)
            print(f"Presentation Layer: Received decrypted & decompressed data -> {decompressed_data}")

            if self.next_layer:
                self.next_layer.receive(decompressed_data)

        except Exception as e:
            print(f"Presentation Layer: Error in processing data -> {e}")

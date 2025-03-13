# All layers inherit this class
class OSILayer:
    def __init__(self, next_layer=None):
        # Classes that inherit OSILayer will need one argument
        # which will become that layer's next layer.
        self.next_layer = next_layer

    def send(self, data):
        # If the next layer exists (is not None)
        # then the data can be sent.
        if self.next_layer:
            self.next_layer.send(data)

    def receive(self, data):
        # If the next layer exists (is not None)
        # then the data can be received.
        if self.next_layer:
            self.next_layer.receive(data)
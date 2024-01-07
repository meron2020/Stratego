class ResponsePacket:
    def __init__(self, data_to_return, client_address):
        self.return_address = client_address
        self.data = data_to_return

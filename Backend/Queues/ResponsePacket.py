class ResponsePacket:
    def __init__(self, board, client_address):
        self.return_address = client_address
        self.data = board

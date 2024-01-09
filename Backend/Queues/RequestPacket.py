class RequestPacket:
    def __init__(self, request_type, player_id, client_address, game_id=None, data=None):
        self.game_id = game_id
        self.return_address = client_address
        self.data = data
        self.request_type = request_type
        self.player_id = player_id

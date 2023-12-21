class RequestPacket:
    def __init__(self, game_id, request_type, data, client_address, player_color):
        self.game_id = game_id
        self.return_address = client_address
        self.data = data
        self.request_type = request_type
        self.player_color = player_color

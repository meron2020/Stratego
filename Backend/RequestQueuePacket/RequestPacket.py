class RequestPacket:
    def __init__(self, game_id, request_type, data, http_process_id, player_color):
        self.game_id = game_id
        self.process_id = http_process_id
        self.data = data
        self.request_type = request_type
        self.player_color = player_color

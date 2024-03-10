import requests


class GameHTTPHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, params, req_type=None):
        address = self.server_address + "/games"
        try:
            if req_type == "g":
                response = requests.get(address, params=params, headers=self.headers)
            elif req_type == "p":
                response = requests.post(address, params=params, headers=self.headers)
            elif req_type == "d":
                response = requests.delete(address, params=params, headers=self.headers)
            else:
                response = requests.put(address, params=params, headers=self.headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def get_board(self, game_id):
        params = {"game_id": game_id, "request_type": 1}
        return self.send_request(params, "g")

    def check_if_my_turn(self, game_id, player_id):
        params = {"game_id": game_id, "request_type": 2, "player_id": player_id}
        return self.send_request(params, "g")

    def check_piece_options(self, game_id, piece_id):
        params = {"game_id": game_id, "request_type": 3, "piece_id": piece_id}
        return self.send_request(params, "g")

    def get_game_state(self, game_id):
        params = {"game_id": game_id, "request_type": 4}
        return self.send_request(params, "g")

    def join_game(self, game_id, player_id):
        params = {"game_id": game_id, "player_id": player_id}
        return self.send_request(params, "p")

    def quit_game(self, game_id, player_id):
        params = {"game_id": game_id, "player_id": player_id}
        return self.send_request(params, "d")

    def send_starting_positions(self, game_id, pieces_to_pos_dict):
        params = {"game_id": game_id, "data": {"pieces_to_pos_dict": pieces_to_pos_dict}}
        return self.send_request(params)

    def piece_act(self, game_id, piece_id, new_pos):
        params = {"game_id": game_id, "data": {"piece_id": piece_id, "new_pos": new_pos}}
        return self.send_request(params)

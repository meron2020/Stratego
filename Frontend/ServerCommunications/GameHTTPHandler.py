import requests


class GameHTTPHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, json, req_type=None):
        address = self.server_address + "/games"
        try:
            if req_type == "g":
                response = requests.get(address, json=json, headers=self.headers)
            elif req_type == "p":
                response = requests.post(address, json=json)
            elif req_type == "d":
                response = requests.delete(address, json=json, headers=self.headers)
            else:
                response = requests.put(address, json=json, headers=self.headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def get_board(self, game_id):
        json = {"game_id": game_id, "request_type_num": 1}
        return self.send_request(json, "g")

    def check_if_my_turn(self, game_id, player_id):
        params = {"game_id": game_id, "request_type_num": 2, "player_id": player_id}
        return self.send_request(params, "g")

    def check_piece_options(self, game_id, piece_id):
        json = {"game_id": game_id, "request_type_num": 3, "data": {"piece_id": piece_id}}
        return self.send_request(json, "g")

    def get_game_state(self, game_id):
        params = {"game_id": game_id, "request_type_num": 4}
        return self.send_request(params, "g")

    def join_game(self, player_id):
        json = {"player_id": player_id}
        return self.send_request(json, "p")

    def quit_game(self, game_id, player_id):
        params = {"game_id": game_id, "player_id": player_id}
        return self.send_request(params, "d")

    def send_starting_positions(self, game_id, pieces_to_pos_dict, player_id):
        json = {"player_id": player_id, "request_type_num": 1, "data": {"pieces_to_pos_dict": pieces_to_pos_dict},
                "game_id": game_id}
        return self.send_request(json)

    def piece_act(self, game_id, piece_id, new_pos):
        json = {"game_id": game_id, "data": {"piece_id": piece_id, "new_pos": new_pos}, "request_type_num": 2}
        return self.send_request(json)

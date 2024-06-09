import requests


class GameHTTPHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.headers = {"Content-Type": "application/json"}

    # Function that takes care of sending the HTTP requests.
    def send_request(self, json, endpoint=None, req_type=None):
        if endpoint:
            address = self.server_address + "/games/" + endpoint
        else:
            address = self.server_address + "/games/ "
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

    # Function to request the board, and the associated piece dictionary.
    def get_board(self, game_id):
        json = {"game_id": game_id}
        return self.send_request(json, "get_board", "g")

    # Function to check if it's the player's turn.
    def check_if_my_turn(self, game_id, player_id):
        json = {"game_id": game_id, "player_id": player_id}
        return self.send_request(json, "my_turn", "g")

    # Functino to get a parameter piece moving options.
    def check_piece_options(self, game_id, piece_id):
        json = {"game_id": game_id, "data": {"piece_id": piece_id}}
        return self.send_request(json, "piece_options", "g")

    def check_setup_pos(self, game_id, player_id):
        json = {"game_id": game_id, "player_id": player_id}
        return self.send_request(json, "setup_pos", "g")

    # Function to get the game state. GameId Parameter.
    def get_game_state(self, game_id):
        json = {"game_id": game_id}
        return self.send_request(json, "game_state", "g")

    # Function to send request to join an available game.
    def join_game(self, player_id):
        json = {"player_id": player_id}
        return self.send_request(json, req_type="p")

    # Function to send request to check if the game ended.
    def check_game_ended(self, game_id):
        json = {"game_id": game_id}
        return self.send_request(json, "game_ended", "g")

    # Function that sends the server a request to set that player's pieces' starting positions.
    def send_starting_positions(self, game_id, pieces_to_pos_dict, player_id):
        json = {"player_id": player_id, "data": {"pieces_to_pos_dict": pieces_to_pos_dict},
                "game_id": game_id}
        return self.send_request(json, "piece_setup")

    # Function that sends the server a request for a piece action.
    def piece_act(self, game_id, piece_id, new_pos):
        json = {"game_id": game_id, "data": {"piece_id": piece_id, "new_pos": new_pos}}
        return self.send_request(json, "piece_action")

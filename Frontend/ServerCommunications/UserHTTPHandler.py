import requests


class UserHTTPHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, json, req_type=None):
        address = self.server_address + "/users"
        try:
            if req_type == "g":
                response = requests.get(address, json=json, headers=self.headers)
            elif req_type == "p":
                response = requests.post(address, json=json, headers=self.headers)
            else:
                response = requests.delete(address, json=json, headers=self.headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def get_stats(self, username):
        json = {"username": username}
        return self.send_request(json, "g")

    def create_user(self, username, password):
        json = {"username": username, "password": password}
        return self.send_request(json, "p")

    def delete_user(self, username):
        json = {"username": username}
        return self.send_request(json)

    def auth(self, username, password):
        address = self.server_address + "/auth"
        json = {"username": username, "password": password}
        try:
            response = requests.post(address, json=json, headers=self.headers)

            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None
import requests


class UserHTTPHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, params, req_type=None):
        address = self.server_address + "/user"
        try:
            if req_type == "g":
                response = requests.get(address, params=params, headers=self.headers)
            elif req_type == "p":
                response = requests.post(address, params=params, headers=self.headers)
            else:
                response = requests.delete(address, params=params, headers=self.headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def get_stats(self, username):
        params = {"username": username}
        return self.send_request(params, "g")

    def create_user(self, username, password):
        params = {"username": username, "password": password}
        return self.send_request(params, "p")

    def delete_user(self, username):
        params = {"username": username}
        return self.send_request(params)


class AuthHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.headers = {"Content-Type": "application/json"}

    def auth(self, username, password):
        address = self.server_address + "/auth"
        params = {"username": username, "password": password}
        try:
            response = requests.post(address, params=params, headers=self.headers)

            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

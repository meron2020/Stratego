import requests


class UserHTTPHandler:
    def __init__(self, server_address):
        self.server_address = server_address
        self.token = None

    def send_request(self, json, req_type=None):
        address = self.server_address + "/users"
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers['Authorization'] = self.token
        try:
            if req_type == "g":
                response = requests.get(address, json=json, headers=headers)
            elif req_type == "p":
                response = requests.post(address, json=json, headers=headers)
            else:
                response = requests.delete(address, json=json, headers=headers)
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
        response = self.send_request(json, "p")
        self.token = response['token']
        return response

    def delete_user(self, username):
        json = {"username": username}
        return self.send_request(json)

    def auth(self, username, password):
        headers = {"Content-Type": "application/json"}
        address = self.server_address + "/auth"
        json = {"username": username, "password": password}
        try:
            response = requests.post(address, json=json, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            response = response.json()
            self.token = response['token']
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

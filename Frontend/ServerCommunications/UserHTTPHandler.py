import requests


class UserHTTPHandler:
    def __init__(self, server_address):
        # Initialize the server address and token
        self.server_address = server_address
        self.token = None

    def send_request(self, json, req_type=None):
        # Set the address endpoint and headers for the request
        address = self.server_address + "/users"
        headers = {"Content-Type": "application/json"}

        # Add authorization token to headers if available
        if self.token:
            headers['Authorization'] = self.token

        # Send request based on the request type
        try:
            if req_type == "g":  # GET request
                response = requests.get(address, json=json, headers=headers)
            elif req_type == "p":  # POST request
                response = requests.post(address, json=json, headers=headers)
            else:  # DELETE request (default)
                response = requests.delete(address, json=json, headers=headers)

            # Raise an HTTPError for bad responses
            response.raise_for_status()

            # Return the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Print the error if request fails
            print(f"Error making request: {e}")
            return None

    def get_stats(self, username):
        # Prepare JSON payload
        json = {"username": username}

        # Send GET request to retrieve user stats
        return self.send_request(json, "g")

    def create_user(self, username, password):
        # Prepare JSON payload
        json = {"username": username, "password": password}

        # Send POST request to create a new user
        response = self.send_request(json, "p")

        # Store the token from the response
        self.token = response['token']

        return response

    def auth(self, username, password):
        # Set headers and address for the authentication request
        headers = {"Content-Type": "application/json"}
        address = self.server_address + "/auth"

        # Prepare JSON payload
        json = {"username": username, "password": password}

        # Send POST request for authentication
        try:
            response = requests.post(address, json=json, headers=headers)

            # Raise an HTTPError for bad responses
            response.raise_for_status()

            # Get the JSON response and store the token
            response = response.json()
            self.token = response['token']

            return response

        except requests.exceptions.RequestException as e:
            # Print the error if request fails
            print(f"Error making request: {e}")
            return None

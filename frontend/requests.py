import requests


class FrontendRequests:
    def __init__(self):
        self.requests = requests

    def post(self, message):
        response = self.requests.post(
            "http://127.0.0.1:8000/tables", json={"message": message}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to connect"

    def get(self):
        response = self.requests.get("http://127.0.0.1:8000/entries")
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to connect"

    def put(self, id_num, message):
        response = requests.put(
            f"http://127.0.0.1:8000/entries/{id_num}", json={"message": message}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to connect"

    def delete(self, id_num):
        response = requests.delete(f"http://127.0.0.1:8000/entries/{id_num}")
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to connect"

    def shutdown(self):
        response = requests.post("http://127.0.0.1:8000/shutdown")
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to connect"

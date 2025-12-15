from automation_exercise.API.client import APIClient


class DeleteAPI:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def delete_account(self, email: str, password: str) -> dict:
        return self.client.request("DELETE", "/deleteAccount", data={"email": email, "password": password})

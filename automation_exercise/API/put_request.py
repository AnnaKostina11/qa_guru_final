from automation_exercise.API.client import APIClient


class PutAPI:
    # Группа PUT-эндпоинтов.

    def __init__(self, client: APIClient) -> None:
        self.client = client

    def update_user_account(self, data: dict) -> dict:
        return self.client.request("PUT", "/updateAccount", data=data)

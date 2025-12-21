from jsonschema import validate

from automation_exercise.API.client import APIClient
from automation_exercise.utils.schemas import DELETE_ACCOUNT_REQUEST_SCHEMA


class DeleteAPI:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def delete_account(self, email: str, password: str) -> dict:
        data = {"email": email, "password": password}

        # Схемы для request
        validate(instance=data, schema=DELETE_ACCOUNT_REQUEST_SCHEMA)

        return self.client.request("DELETE", "/deleteAccount", data=data)

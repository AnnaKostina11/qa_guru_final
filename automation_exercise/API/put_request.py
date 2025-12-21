from jsonschema import validate

from automation_exercise.API.client import APIClient
from automation_exercise.utils.schemas import UPDATE_ACCOUNT_REQUEST_SCHEMA


class PutAPI:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def update_user_account(self, data: dict) -> dict:
        # Схемы для request
        validate(instance=data, schema=UPDATE_ACCOUNT_REQUEST_SCHEMA)

        return self.client.request("PUT", "/updateAccount", data=data)

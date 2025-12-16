from jsonschema import validate

from automation_exercise.API.client import APIClient
from automation_exercise.utils.attach import attach_json
from automation_exercise.utils.schemas import DELETE_ACCOUNT_REQUEST_SCHEMA


class DeleteAPI:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def delete_account(self, email: str, password: str) -> dict:
        data = {"email": email, "password": password}

        attach_json("request.validated_schema", DELETE_ACCOUNT_REQUEST_SCHEMA)
        validate(instance=data, schema=DELETE_ACCOUNT_REQUEST_SCHEMA)
        return self.client.request("DELETE", "/deleteAccount", data=data)

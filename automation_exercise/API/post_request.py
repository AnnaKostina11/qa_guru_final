from jsonschema import validate

from automation_exercise.API.client import APIClient
from automation_exercise.utils.schemas import (
    CREATE_ACCOUNT_REQUEST_SCHEMA,
    VERIFY_LOGIN_REQUEST_SCHEMA,
)


class PostAPI:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def create_account(self, user) -> dict:
        data = {
            "name": user.nick_name,
            "email": user.email,
            "password": user.password,
            "title": "Mr",
            "birth_date": user.day,
            "birth_month": user.month,
            "birth_year": user.year,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "company": user.company_name,
            "address1": user.first_address,
            "address2": user.second_address,
            "country": user.country,
            "zipcode": user.zipcode,
            "city": user.city,
            "state": user.state,
            "mobile_number": user.mobile_number,
        }

        # Схемы для request
        validate(instance=data, schema=CREATE_ACCOUNT_REQUEST_SCHEMA)

        return self.client.request("POST", "/createAccount", data=data)

    def verify_login(self, user) -> dict:
        data = {"email": user.email, "password": user.password}

        # Схемы для request
        validate(instance=data, schema=VERIFY_LOGIN_REQUEST_SCHEMA)

        return self.client.request("POST", "/verifyLogin", data=data)

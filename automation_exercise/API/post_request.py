from automation_exercise.API.client import APIClient


class PostAPI:
    # Группа POST-эндпоинтов.
    # Каждый метод возвращает response_info (см. APIClient.request),
    # чтобы дальше его проверял BaseTestRequests.check_response().

    def __init__(self, client: APIClient) -> None:
        self.client = client

    def create_account(self, user) -> dict:
        # Формируем body для /createAccount из модели User.
        # Используем "data" (form-data / x-www-form-urlencoded), как ожидает API automationexercise.
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

        return self.client.request("POST", "/createAccount", data=data)

    def verify_login(self, user) -> dict:
        # /verifyLogin принимает только email/password.
        data = {"email": user.email, "password": user.password}
        return self.client.request("POST", "/verifyLogin", data=data)

import allure
from allure_commons.types import Severity

from automation_exercise.API.api_manager import APIManager
from automation_exercise.utils.base_test_request import BaseTestRequests


class TestVerifyLogin(BaseTestRequests):

    @allure.id("02_POST_REQUEST")
    @allure.tag("API", "POST")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("POST")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_valid_status_code(self, create_user):
        api = APIManager()

        with allure.step("Создать пользователя через API (POST createAccount)"):
            api.post.create_account(create_user)

        with allure.step("Отправить запрос проверки логина (POST verifyLogin)"):
            response_info = api.post.verify_login(create_user)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

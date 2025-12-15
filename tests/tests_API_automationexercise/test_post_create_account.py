import json
import allure
from allure_commons.types import Severity

from automation_exercise.API.api_manager import APIManager
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage


class TestCreateAccount(BaseTestRequests):

    @allure.id("01_POST_REQUEST")
    @allure.tag("API", "POST")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("POST")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_successful_account_creation(self, create_user):
        api = APIManager()

        with allure.step("Создать аккаунт через API (POST createAccount)"):
            response_info = api.post.create_account(create_user)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 201)

        with allure.step("Проверить сообщение о создании пользователя"):
            response = response_info.get("response")
            # у тебя иногда message приходит как JSON-строка внутри JSON
            message_raw = response["message"]
            nested_message = json.loads(message_raw) if isinstance(message_raw, str) else message_raw

            assert nested_message["message"] == StatusMessage.post_user_created

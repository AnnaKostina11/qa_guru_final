import json

import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage


class TestCreateAccount(BaseTestRequests):

    @allure.id("01_POST_REQUEST")
    @allure.tag("API", "POST")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("POST")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_successful_account_creation(self, api_application, create_user):
        with allure.step("Создать аккаунт через API (POST createAccount)"):
            response_info = api_application.post.create_account(create_user)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 201)

        with allure.step("Распарсить тело ответа (response) в JSON"):
            response_json_str = response_info.get("response")
            response_json = (
                json.loads(response_json_str)
                if isinstance(response_json_str, str)
                else response_json_str
            )
            assert isinstance(response_json, dict), "Ответ должен быть JSON-объектом (dict)"
            assert "message" in response_json, "В ответе отсутствует поле message"

        with allure.step("Распарсить вложенное сообщение из поля message"):
            nested_message_str = response_json["message"]
            nested_message_json = json.loads(nested_message_str)
            assert isinstance(nested_message_json, dict), "Вложенное сообщение должно быть JSON-объектом (dict)"
            assert "message" in nested_message_json, "Во вложенном сообщении нет поля message"

        with allure.step(f"Проверить текст сообщения = {StatusMessage.post_user_created}"):
            assert nested_message_json["message"] == StatusMessage.post_user_created

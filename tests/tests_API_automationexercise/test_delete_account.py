import json

import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage


class TestUserAccount(BaseTestRequests):

    @allure.id("05_DELETE_REQUEST")
    @allure.tag("API", "DELETE")
    @allure.severity(Severity.MINOR)
    @allure.parent_suite("API")
    @allure.suite("DELETE")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_valid_status_code(self, api_application, create_user):
        with allure.step("Создать пользователя через API"):
            api_application.post.create_account(create_user)

        with allure.step("Отправить DELETE-запрос на удаление пользователя"):
            response_info = api_application.delete.user_account(create_user)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

    @allure.id("02_DELETE_REQUEST")
    @allure.tag("API", "DELETE")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("DELETE")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_verify_response_message(self, api_application, create_user):
        with allure.step("Создать пользователя через API"):
            api_application.post.create_account(create_user)

        with allure.step("Отправить DELETE-запрос на удаление пользователя"):
            response_info = api_application.delete.user_account(create_user)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

        with allure.step("Распарсить тело ответа (response) в JSON"):
            response_json_str = response_info.get("response")
            response_json = (
                json.loads(response_json_str)
                if isinstance(response_json_str, str)
                else response_json_str
            )
            assert isinstance(response_json, dict), "Ответ должен быть JSON-объектом (dict)"

        with allure.step("Извлечь вложенное сообщение из поля message"):
            nested_message_str = response_json["message"]
            nested_message_json = json.loads(nested_message_str)
            assert "message" in nested_message_json, "Во вложенном сообщении нет поля message"

        with allure.step(f"Проверить текст сообщения = {StatusMessage.del_account_deleted}"):
            assert nested_message_json["message"] == StatusMessage.del_account_deleted

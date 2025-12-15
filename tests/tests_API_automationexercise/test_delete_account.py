import json
import allure
from allure_commons.types import Severity

from automation_exercise.API.api_manager import APIManager
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage


class TestUserAccount(BaseTestRequests):

    @allure.id("05_DELETE_REQUEST")
    @allure.tag("API", "DELETE")
    @allure.severity(Severity.MINOR)
    @allure.parent_suite("API")
    @allure.suite("DELETE")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_valid_status_code(self, create_user):
        api = APIManager()

        with allure.step("Создать пользователя через API"):
            api.post.create_account(create_user)

        with allure.step("Отправить DELETE-запрос на удаление пользователя"):
            response_info = api.delete.delete_account(create_user.email, create_user.password)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

    @allure.id("02_DELETE_REQUEST")
    @allure.tag("API", "DELETE")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("DELETE")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_verify_response_message(self, create_user):
        api = APIManager()

        with allure.step("Создать пользователя через API"):
            api.post.create_account(create_user)

        with allure.step("Отправить DELETE-запрос на удаление пользователя"):
            response_info = api.delete.delete_account(create_user.email, create_user.password)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

        with allure.step(f"Проверить сообщение успешного удаления = {StatusMessage.del_account_deleted}"):
            response = response_info.get("response")
            message_raw = response["message"]
            nested_message = json.loads(message_raw) if isinstance(message_raw, str) else message_raw

            assert nested_message["message"] == StatusMessage.del_account_deleted

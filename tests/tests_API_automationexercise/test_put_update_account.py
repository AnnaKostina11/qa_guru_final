import json
import allure
from allure_commons.types import Severity

from automation_exercise.API.api_manager import APIManager
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage


class TestUpdateUserAccount(BaseTestRequests):

    @allure.id("03_PUT_REQUEST")
    @allure.tag("API", "PUT")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("PUT")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_verify_response_message(self, create_user_account, update_user_params):
        api = APIManager()

        with allure.step("Выполнить PUT-запрос на обновление аккаунта пользователя"):
            response_info = api.put.update_user_account(update_user_params)

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

        with allure.step(f"Проверить сообщение об успешном обновлении = {StatusMessage.put_user_update}"):
            response = response_info.get("response")
            message_raw = response["message"]
            nested_message = json.loads(message_raw) if isinstance(message_raw, str) else message_raw

            assert nested_message["message"] == StatusMessage.put_user_update

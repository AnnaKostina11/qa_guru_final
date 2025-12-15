import json
import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.schemas import MESSAGE_ONLY_SCHEMA
from automation_exercise.utils.static_values import StatusMessage


class TestUpdateUserAccount(BaseTestRequests):

    @allure.id("03_PUT_REQUEST")
    @allure.tag("API", "PUT")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("PUT")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_verify_response_message(self, api_application, create_user_account, update_user_params):
        with allure.step("Выполнить PUT-запрос на обновление аккаунта пользователя"):
            response_info = api_application.put.update_user_account(update_user_params)

        with allure.step("Проверить HTTP статус, business responseCode и схему"):
            body = self.check_response_status_and_message_business_code(
                response_info, expected_http=200, expected_business=200, schema=MESSAGE_ONLY_SCHEMA
            )

        with allure.step(f"Проверить сообщение об успешном обновлении = {StatusMessage.put_user_update}"):
            nested = json.loads(body["message"]) if isinstance(body["message"], str) else body["message"]
            assert nested["message"] == StatusMessage.put_user_update

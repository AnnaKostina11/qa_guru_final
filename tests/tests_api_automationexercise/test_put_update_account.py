import allure
from allure_commons.types import Severity

from automation_exercise.data.api_responses import MessageOnlyResponse
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.schemas import MESSAGE_ONLY_SCHEMA
from automation_exercise.utils.static_values import StatusMessage


@allure.epic("API")
@allure.feature("Put")
@allure.story("Update account")
class TestUpdateUserAccount(BaseTestRequests):

    @allure.tag("API", "REGRESS")
    @allure.label("layer", "api")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Обновление аккаунта пользователя.")
    def test_verify_response_message(self, api_application, create_user_account, update_user_params):
        with allure.step("Выполнить PUT-запрос на обновление аккаунта пользователя"):
            response_info = api_application.put.update_user_account(update_user_params)

        with allure.step("Проверить HTTP статус, business responseCode, схему и десериализацию"):
            resp = self.check_response(
                response_info=response_info,
                expected_http=200,
                expected_business=200,
                schema=MESSAGE_ONLY_SCHEMA,
                model_cls=MessageOnlyResponse,
            )

        with allure.step(f"Проверить сообщение об успешном обновлении = {StatusMessage.put_user_update}"):
            assert resp.message == StatusMessage.put_user_update

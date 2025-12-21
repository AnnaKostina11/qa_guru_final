import allure
from allure_commons.types import Severity

from automation_exercise.data.api_responses import MessageOnlyResponse
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.schemas import MESSAGE_ONLY_SCHEMA
from automation_exercise.utils.static_values import StatusMessage


@allure.epic("API")
@allure.feature("Post")
@allure.story("Login to account")
class TestVerifyLogin(BaseTestRequests):

    @allure.tag("API", "REGRESS")
    @allure.label("layer", "api")
    @allure.severity(Severity.CRITICAL)
    @allure.title("Проверка авторизации.")
    def test_valid_status_code(self, api_application, create_user):
        with allure.step("Создать пользователя через API"):
            api_application.post.create_account(create_user)

        with allure.step("Проверить логин через API (verifyLogin)"):
            response_info = api_application.post.verify_login(create_user)

        with allure.step("Проверить HTTP статус, business responseCode, схему и десериализацию"):
            resp = self.check_response(
                response_info=response_info,
                expected_http=200,
                expected_business=200,
                schema=MESSAGE_ONLY_SCHEMA,
                model_cls=MessageOnlyResponse,
            )

        with allure.step(f"Проверить сообщение успешного логина = {StatusMessage.post_user_exists}"):
            assert resp.message == StatusMessage.post_user_exists

import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.schemas import MESSAGE_ONLY_SCHEMA
from automation_exercise.utils.static_values import StatusMessage


class TestVerifyLogin(BaseTestRequests):

    @allure.id("02_POST_REQUEST")
    @allure.tag("API", "POST")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("POST")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_valid_status_code(self, api_application, create_user):
        with allure.step("Создать пользователя через API"):
            api_application.post.create_account(create_user)

        with allure.step("Проверить логин через API (verifyLogin)"):
            response_info = api_application.post.verify_login(create_user)

        with allure.step("Проверить HTTP статус, business responseCode и схему"):
            body = self.check_response_status_and_message_business_code(
                response_info,
                expected_http=200,
                expected_business=200,
                schema=MESSAGE_ONLY_SCHEMA,
            )

        with allure.step(f"Проверить сообщение успешного логина = {StatusMessage.post_user_exists}"):
            assert body.get("message") == StatusMessage.post_user_exists

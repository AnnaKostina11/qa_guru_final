import allure
from allure_commons.types import Severity

from automation_exercise.data.api_responses import MessageOnlyResponse
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.schemas import MESSAGE_ONLY_SCHEMA
from automation_exercise.utils.static_values import StatusMessage


class TestUserAccount(BaseTestRequests):

    @allure.id("05_DELETE_REQUEST")
    @allure.tag("API", "DELETE")
    @allure.severity(Severity.MINOR)
    @allure.parent_suite("API")
    @allure.suite("DELETE")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    @allure.title("Удаление пользователя.")
    def test_verify_response_message(self, api_application, create_user):
        with allure.step("Создать пользователя через API"):
            api_application.post.create_account(create_user)

        with allure.step("Удалить пользователя через API"):
            response_info = api_application.delete.delete_account(create_user.email, create_user.password)

        with allure.step("Проверить HTTP статус, business responseCode, схему и десериализацию"):
            resp = self.check_response(
                response_info=response_info,
                expected_http=200,
                expected_business=200,
                schema=MESSAGE_ONLY_SCHEMA,
                model_cls=MessageOnlyResponse,
            )

        with allure.step(f"Проверить сообщение успешного удаления = {StatusMessage.del_account_deleted}"):
            assert resp.message == StatusMessage.del_account_deleted

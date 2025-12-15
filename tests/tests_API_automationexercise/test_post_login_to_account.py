import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests


class TestVerifyLogin(BaseTestRequests):

    @allure.id('02_POST_REQUEST')
    @allure.tag('API', 'POST')
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite('API')
    @allure.suite('POST')
    @allure.link('https://www.automationexercise.com', name='Testing API')
    def test_valid_status_code(self, api_application, create_user):
        api_application.post.create_account(create_user)
        response_info = api_application.post.verify_login(create_user)
        self.check_response_status_and_message_business_code(response_info, 200, 200)

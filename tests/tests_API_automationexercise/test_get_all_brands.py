import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests


class TestAllBrands(BaseTestRequests):

    @allure.id('04_GET_REQUEST')
    @allure.tag('API', 'GET')
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite('API')
    @allure.suite('GET')
    @allure.link('https://www.automationexercise.com', name='Testing API')
    def test_valid_status_code(self, api_application):
        response_info = api_application.get.all_brand_list()
        self.check_response_status_and_message_business_code(response_info, 200, 200)

import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.schemas import BRANDS_LIST_SCHEMA


class TestAllBrands(BaseTestRequests):

    @allure.id("04_GET_REQUEST")
    @allure.tag("API", "GET")
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite("API")
    @allure.suite("GET")
    @allure.link("https://www.automationexercise.com", name="Testing API")
    def test_valid_status_code(self, api_application):
        with allure.step("Отправить GET-запрос на получение списка брендов"):
            response_info = api_application.get.all_brand_list()

        with allure.step("Проверить HTTP статус, business responseCode и схему"):
            body = self.check_response_status_and_message_business_code(
                response_info, expected_http=200, expected_business=200, schema=BRANDS_LIST_SCHEMA
            )

        with allure.step("Проверить, что brands не пустой"):
            assert len(body["brands"]) > 0

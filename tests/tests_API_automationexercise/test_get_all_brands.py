import json
import allure
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests


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

        with allure.step("Проверить HTTP статус-код и бизнес-код ответа"):
            self.check_response_status_and_message_business_code(response_info, 200, 200)

            # если в dict хранится реальный HTTP код
            # (название ключа может отличаться — смотри как устроен твой BaseTestRequests)
            http_status = response_info.get("status_code") or response_info.get("status")
            assert http_status == 200, f"Неожиданный HTTP статус: {http_status}"

        with allure.step("Проверить, что ответ в формате JSON"):
            response_json_raw = response_info.get("response")
            body = json.loads(response_json_raw) if isinstance(response_json_raw, str) else response_json_raw
            assert isinstance(body, dict), "JSON-ответ должен быть объектом (dict)"

        with allure.step("Проверить наличие и значение поля responseCode"):
            assert "responseCode" in body, "В ответе отсутствует поле responseCode"
            assert body["responseCode"] == 200, f"Неожиданный responseCode: {body['responseCode']}"

        with allure.step("Проверить, что список brands присутствует и не пустой"):
            assert "brands" in body, "В ответе отсутствует поле brands"
            assert isinstance(body["brands"], list), "Поле brands должно быть списком"
            assert len(body["brands"]) > 0, "Список brands не должен быть пустым"

        with allure.step("Проверить структуру первого элемента brands"):
            first = body["brands"][0]
            assert isinstance(first, dict), "Элемент brands должен быть объектом (dict)"
            assert "brand" in first, "В элементе brands отсутствует поле brand"
            assert isinstance(first["brand"], str) and first["brand"].strip(), "Поле brand должно быть непустой строкой"

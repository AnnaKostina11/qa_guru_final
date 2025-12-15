from allure import step
from jsonschema import validate


class BaseTestRequests:
    def check_response_status_and_message_business_code(
        self,
        response_info: dict,
        expected_http: int,
        expected_business: int,
        schema: dict | None = None,
    ) -> dict:
        with step(f"Проверка HTTP статус-кода = {expected_http}"):
            assert response_info["status_code"] == expected_http, response_info

        body = response_info.get("response")
        with step("Проверка, что response — JSON объект (dict)"):
            assert isinstance(body, dict), f"response must be dict, got: {type(body)}"

        with step(f"Проверка business responseCode = {expected_business}"):
            assert body.get("responseCode") == expected_business, body

        if schema is not None:
            with step("Валидация ответа по JSON Schema"):
                validate(instance=body, schema=schema)

        return body

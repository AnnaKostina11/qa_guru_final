import json
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

        with step("Проверка и нормализация response в dict"):
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except Exception as e:
                    raise AssertionError(f"response is str and not JSON: {body[:300]}") from e

            assert isinstance(body, dict), f"response must be dict, got: {type(body)}"

            if "responseCode" not in body and isinstance(body.get("message"), str):
                msg = body["message"].strip()
                if msg.startswith("{") and msg.endswith("}"):
                    try:
                        body = json.loads(msg)
                    except Exception as e:
                        raise AssertionError(f'Body["message"] looks like JSON but not parsed: {msg[:300]}') from e

        with step(f"Проверка business responseCode = {expected_business}"):
            assert body.get("responseCode") == expected_business, body

        if schema is not None:
            with step("Валидация ответа по JSON Schema"):
                validate(instance=body, schema=schema)

        return body

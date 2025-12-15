import json
from typing import Any, Callable, TypeVar

from allure import step
from jsonschema import validate

T = TypeVar("T")


class BaseTestRequests:
    def check_response(
        self,
        response_info: dict,
        expected_http: int,
        expected_business: int,
        schema: dict | None = None,
        model_cls: type[T] | None = None,
        from_dict: Callable[[dict[str, Any]], T] | None = None,
    ) -> dict | T:
        """
        Единая точка проверки ответа:
        - HTTP status
        - нормализация response в dict (в т.ч. вложенный JSON в поле message)
        - business responseCode
        - JSON Schema
        - (опционально) десериализация в модель

        Модель поддерживается в двух вариантах:
        1) model_cls имеет classmethod from_dict(data) -> T
        2) передан from_dict callable
        """
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

            # Если сервер/клиент завернул JSON-ответ внутрь поля "message"
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

        if model_cls is None and from_dict is None:
            return body

        with step("Десериализация ответа в модель"):
            if from_dict is not None:
                return from_dict(body)

            # model_cls.from_dict(body)
            if not hasattr(model_cls, "from_dict"):
                raise AssertionError("model_cls must have from_dict(data: dict) method")
            return model_cls.from_dict(body)  # type: ignore[attr-defined]

    # Для обратной совместимости (если где-то уже вызывается старое имя)
    def check_response_status_and_message_business_code(
        self,
        response_info: dict,
        expected_http: int,
        expected_business: int,
        schema: dict | None = None,
    ) -> dict:
        return self.check_response(
            response_info=response_info,
            expected_http=expected_http,
            expected_business=expected_business,
            schema=schema,
        )

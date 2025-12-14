from allure import step

class BaseTestRequests:
    def check_response_status_and_message_business_code(self, response_info, expected_http, expected_business):
        with step(f"Проверка HTTP статуса: ожидаем {expected_http}"):
            assert response_info["status_code"] == expected_http
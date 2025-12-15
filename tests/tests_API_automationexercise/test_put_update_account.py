import json

import allure
from allure import step
from allure_commons.types import Severity

from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage


class TestUpdateUserAccount(BaseTestRequests):

    @allure.id('03_PUT_REQUEST')
    @allure.tag('API', 'PUT')
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite('API')
    @allure.suite('PUT')
    @allure.link('https://www.automationexercise.com', name='Testing API')
    def test_verify_response_message(self, api_application, create_user, update_user_params, create_user_account):
        with step(f'Выполняем запрос'):
            response_info = api_application.put.update_user_account(update_user_params)

        self.check_response_status_and_message_business_code(response_info, 200, 200)

        with step(f'Сообщение об успешном обновлении = {StatusMessage.put_user_update}'):
            response_json_str = response_info.get('response')
            response_json = json.loads(response_json_str) if isinstance(response_json_str, str) else response_json_str

            nested_message_str = response_json['message']
            nested_message_json = json.loads(nested_message_str)

            assert nested_message_json['message'] == StatusMessage.put_user_update

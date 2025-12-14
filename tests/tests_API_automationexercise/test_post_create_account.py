import allure
import json
from allure import step
from allure_commons.types import Severity
from automation_exercise.utils.base_test_request import BaseTestRequests
from automation_exercise.utils.static_values import StatusMessage

class TestCreateAccount(BaseTestRequests):

    @allure.id('01_POST_REQUEST')
    @allure.tag('API', 'POST')
    @allure.severity(Severity.NORMAL)
    @allure.parent_suite('API')
    @allure.suite('POST')
    @allure.link('https://www.automationexercise.com', name='Testing API')
    def test_successful_account_creation(self, api_application, create_user):
        with step('Создаем аккаунт через API'):
            response_info = api_application.post.create_account(create_user)

        with step(f'Проверяем код ответа и сообщение = {StatusMessage.post_user_created}'):
            self.check_response_status_and_message_business_code(response_info, 200, 201)

            response_json_str = response_info.get('response')
            response_json = json.loads(response_json_str) if isinstance(response_json_str, str) else response_json_str

            nested_message_str = response_json['message']
            nested_message_json = json.loads(nested_message_str)

            assert nested_message_json['message'] == StatusMessage.post_user_created

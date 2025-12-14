import os
import allure
import pytest
from selene.support.shared import browser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from automation_exercise.utils import attach


@allure.title('Инициализация браузера.')
@pytest.fixture(scope='function', autouse=True)
def manage_browser(request):
    browser.config.base_url = os.getenv('BASE_URL')
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    is_remote = request.config.getoption('--remote')

    if is_remote:
        selenoid_login = os.getenv('SELENOID_LOGIN')
        selenoid_pass = os.getenv('SELENOID_PASS')
        selenoid_url = os.getenv('SELENOID_URL')
        selenoid_capabilities = {
            'browserName': 'chrome',
            'browserVersion': '128.0',
            'selenoid:options': {
                'enableVideo': True
            }
        }

        options = Options()
        options.capabilities.update(selenoid_capabilities)

        browser.config.driver = webdriver.Remote(
            command_executor=f'https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub',
            options=options
        )

    yield

    attach.screenshot()
    attach.logs()
    attach.html()

    if is_remote:
        attach.add_video(browser)

    browser.quit()
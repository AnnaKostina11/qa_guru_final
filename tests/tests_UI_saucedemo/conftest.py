import json
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        item.status = "failed"
    else:
        item.status = "passed"


@pytest.fixture(scope="class")
def browser(request):
    chrome_options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    if hasattr(request.node, 'status') and request.node.status == "failed":
        allure.attach(
            name="screenshot",
            body=driver.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG,
        )
    driver.quit()


@pytest.fixture(scope="class")
def log_in_saucedemo(browser):
    from pages.authorization_page import AuthorizationPage
    from pages.home_page import HomePage
    auth = AuthorizationPage(browser)
    auth.open_authorization_page()
    auth.fill_username(config.SAUCEDEMO_LOGIN)
    auth.fill_password(config.SAUCEDEMO_PASSWORD)
    auth.submit()
    HomePage(browser).verify_url()
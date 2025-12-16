import os
from pathlib import Path

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_BROWSER_VERSION = ""


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def _attach_screenshot():
    try:
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="Screenshot",
            attachment_type=AttachmentType.PNG,
        )
    except Exception:
        pass


def _attach_page_source():
    try:
        allure.attach(
            browser.driver.page_source,
            name="PageSource",
            attachment_type=AttachmentType.HTML,
        )
    except Exception:
        pass


def _attach_browser_logs():
    try:
        logs = browser.driver.get_log("browser")
        text = "\n".join(str(x) for x in logs)
        allure.attach(text, name="Browser console logs", attachment_type=AttachmentType.TEXT)
    except Exception:
        pass


def _build_video_url(session_id: str) -> str | None:
    selenoid_ui = (os.getenv("SELENOID_UI") or "").rstrip("/")
    if selenoid_ui:
        return f"{selenoid_ui}/video/{session_id}.mp4"

    raw = (os.getenv("SELENOID_URL") or "").strip()
    if not raw:
        return None

    raw = raw.replace("/wd/hub", "").rstrip("/")
    if not raw.startswith("http://") and not raw.startswith("https://"):
        raw = "http://" + raw

    return f"{raw}/video/{session_id}.mp4"


def _attach_video():
    try:
        session_id = browser.driver.session_id
    except Exception:
        return

    video_url = _build_video_url(session_id)
    if not video_url:
        return

    try:
        allure.attach(video_url, name="Video URL", attachment_type=AttachmentType.URI_LIST)
    except Exception:
        pass

    try:
        target = Path("artifacts") / f"{session_id}.mp4"
        target.parent.mkdir(parents=True, exist_ok=True)

        r = requests.get(video_url, timeout=40)
        r.raise_for_status()
        target.write_bytes(r.content)

        allure.attach.file(str(target), name="Video", attachment_type=AttachmentType.MP4)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    _attach_screenshot()
    _attach_page_source()
    _attach_browser_logs()
    _attach_video()


def _create_chrome_options(browser_version: str) -> Options:
    options = Options()

    options.set_capability("browserName", "chrome")
    if browser_version:
        options.set_capability("browserVersion", browser_version)

    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    options.set_capability("acceptInsecureCerts", True)

    # Убираем попапы Chrome Password Manager / “Change password”
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    return options


def _make_remote_driver(options: Options) -> webdriver.Remote:
    url = (os.getenv("SELENOID_URL") or "").strip()
    if not url:
        raise RuntimeError("SELENOID_URL is required for remote run")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASS")
    if login and password:
        scheme, rest = url.split("://", 1)
        url = f"{scheme}://{login}:{password}@{rest}"

    # Для контейнера
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.set_capability(
        "selenoid:options",
        {"enableVNC": True, "enableVideo": True, "enableLog": True},
    )

    return webdriver.Remote(command_executor=url, options=options)


@pytest.fixture(scope="function", autouse=True)
def browser_setup():
    # Надёжный выбор режима:
    # 1) если RUN_MODE=selenoid -> remote
    # 2) иначе, если SELENOID_URL задан -> тоже remote (чтобы CI не запускал локальный Chrome)
    run_mode = (os.getenv("RUN_MODE") or "").strip().lower()
    selenoid_url = (os.getenv("SELENOID_URL") or "").strip()

    use_remote = (run_mode == "selenoid") or bool(selenoid_url)

    browser_version = (os.getenv("BROWSER_VERSION") or DEFAULT_BROWSER_VERSION).strip()
    browser.config.timeout = float(os.getenv("UI_TIMEOUT", "6.0"))
    browser.config.base_url = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com").rstrip("/")

    width = int(os.getenv("UI_WIDTH", "1920"))
    height = int(os.getenv("UI_HEIGHT", "1080"))

    options = _create_chrome_options(browser_version)

    if use_remote:
        driver = _make_remote_driver(options)
    else:
        driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.driver.set_window_size(width, height)

    yield browser

    browser.quit()

import logging
import os

import pytest
from dotenv import load_dotenv
from selene.support.shared import browser

from automation_exercise.data.user import User, UserCard
from automation_exercise.utils.static_values import Country, Months


# Один раз за сессию подгружаем переменные окружения из .env
@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


# Глобальная настройка форматирования логов для всех модулей проекта
@pytest.fixture(scope="session", autouse=True)
def configure_console_logging():
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="-%Y-%m-%d %H:%M:%S",
    )


# Устанавливаем базовый URL API в browser.config.base_url для единой точки конфигурации
@pytest.fixture(scope="session", autouse=True)
def set_api_base_url():
    browser.config.base_url = os.getenv(
        "AUTOMATIONEXERCISE_API_URL",
        "https://www.automationexercise.com/api",
    ).rstrip("/")


# Возвращаем текущий base_url API для переиспользования в API-клиенте
@pytest.fixture(scope="session")
def api_base_url() -> str:
    return browser.config.base_url


# Создаем экземпляр APIManager с нужным base_url для каждого теста
@pytest.fixture(scope="function")
def api_application(api_base_url):
    from automation_exercise.API.api_manager import APIManager
    return APIManager(base_url=api_base_url)


# Формируем тестового пользователя с полным набором полей профиля и адреса
@pytest.fixture(scope="function")
def create_user():
    user = User(
        nick_name="Trigive",
        email="SomogyiAlbert@jourrapide.com",
        password="Tud6shi0s",
        company_name="Grossman's",
        country=Country.Hungary.value,
        first_name="Albert",
        last_name="Somogyi",
        gender="male",
        day="10",
        month=Months.may.value[0],
        year="1972",
        city="Fertôd",
        state="Nyugat-Dunántúl",
        first_address="Wesselényi u. 38.",
        second_address="Wesselényi u. 38.",
        zipcode="9433",
        mobile_number="899116581",
    )

    user_card = UserCard(
        name=f"{user.first_name.upper()} {user.last_name}",
        number="4539862908251239",
        cvc="916",
        expiration_month="09",
        expiration_year="2026",
    )

    user.add_card(user_card)
    return user


# Создаем аккаунт пользователя и удаляем после завершения теста
@pytest.fixture(scope="function")
def create_user_account(api_application, create_user):
    api_application.delete.delete_account(create_user.email, create_user.password)
    yield api_application.post.create_account(create_user)
    api_application.delete.delete_account(create_user.email, create_user.password)


# Набор данных для запроса обновления профиля пользователя
@pytest.fixture(scope="function")
def update_user_params(create_user):
    return {
        "firstname": "UpdatedName",
        "lastname": "UpdatedLastName",
        "email": create_user.email,
        "password": create_user.password,
    }


# Готовим пользователя для логина
@pytest.fixture(scope="function")
def ui_login_user(api_application, create_user):
    api_application.delete.delete_account(create_user.email, create_user.password)
    api_application.post.create_account(create_user)
    return create_user

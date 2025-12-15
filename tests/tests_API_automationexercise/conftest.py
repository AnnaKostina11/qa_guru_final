import os
import pytest
from dotenv import load_dotenv

from automation_exercise.data.user import User, UserCard
from automation_exercise.utils.static_values import Country, Months


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("AUTOMATIONEXERCISE_API_URL", "https://www.automationexercise.com/api").rstrip("/")


@pytest.fixture(scope="function")
def api_application(api_base_url):
    from automation_exercise.API.api_manager import APIManager
    return APIManager(base_url=api_base_url)


@pytest.fixture(scope="function")
def create_user():
    user = User(
        nick_name="Testovich",
        email="testov2_qaguru@test.com",
        password="Qwe123",
        company_name="Trevor Corporation",
        country=Country.india.value,
        first_name="Trevor",
        last_name="Laxtin",
        gender="male",
        day="10",
        month=Months.may.value[0],
        year="2000",
        city="Bangladesh",
        state="Salavalas",
        first_address="Shampte 32 str., appartment 33",
        second_address="Helentors 5 str., apartment 44",
        zipcode="2331144",
        mobile_number="34534222323",
    )

    user_card = UserCard(
        name=f"{user.first_name.upper()} {user.last_name}",
        number="5677654433225566",
        cvc="111",
        expiration_month="02",
        expiration_year="2030",
    )
    user.add_card(user_card)
    return user


@pytest.fixture(scope="function")
def create_user_account(api_application, create_user):
    api_application.delete.delete_account(create_user.email, create_user.password)
    yield api_application.post.create_account(create_user)
    api_application.delete.delete_account(create_user.email, create_user.password)


@pytest.fixture(scope="function")
def update_user_params(create_user):
    return {
        "firstname": "UpdatedName",
        "lastname": "UpdatedLastName",
        "email": create_user.email,
        "password": create_user.password,
    }


@pytest.fixture(scope="function")
def ui_login_user(api_application, create_user):
    """
    Подготовка сущности для UI: гарантируем, что пользователь существует.
    (Если UI проект будет логиниться через форму, ему нужен валидный аккаунт.)
    """
    api_application.delete.delete_account(create_user.email, create_user.password)
    api_application.post.create_account(create_user)
    return create_user

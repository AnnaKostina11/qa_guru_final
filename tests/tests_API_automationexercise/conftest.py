import pytest

from automation_exercise.API.delete_request import delete_account
from automation_exercise.API.post_request import post_create_account
from automation_exercise.data.user import User, UserCard
from automation_exercise.utils.static_values import Country, Months


@pytest.fixture(scope='function')
def create_user():
    user = User(
        nick_name='Testovich',
        email='testov2_qaguru@test.com',
        password='Qwe123',
        company_name='Trevor Corporation',
        country=Country.india.value,
        first_name='Trevor',
        last_name='Laxtin',
        gender='male',
        day='10',
        month=Months.may.value[0],
        year='2000',
        city='Bangladesh',
        state='Salavalas',
        first_address='Shampte 32 str., appartment 33',
        second_address='Helentors 5 str., apartment 44',
        zipcode='2331144',
        mobile_number='34534222323'
    )
    user_card = UserCard(
        name=f'{user.first_name.upper()} {user.last_name}',
        number='5677654433225566',
        cvc='111',
        expiration_month='02',
        expiration_year='2030'
    )
    user.add_card(user_card)
    return user


@pytest.fixture(scope='function')
def create_user_account(create_user):
    delete_account(create_user.email, create_user.password)
    yield post_create_account(create_user)
    delete_account(create_user.email, create_user.password)


@pytest.fixture(scope='function')
def api_application():
    from automation_exercise.app import APIManager
    return APIManager()


@pytest.fixture(scope='function')
def update_user_params(create_user):
    return {
        'firstname': 'UpdatedName',
        'lastname': 'UpdatedLastName',
        'email': create_user.email,
        'password': create_user.password
    }

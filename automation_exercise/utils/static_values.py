from enum import Enum


class Country(Enum):
    # Значения справочников, которые используются в моделях/фикстурах
    india = "India"


class Months(Enum):
    # Месяц хранится парой (номер, человеко-читаемое название)
    may = ("5", "May")


class StatusMessage:
    # Ожидаемые сообщения от API, используем как единый источник правды в тестах
    post_user_created = "User created!"
    del_account_deleted = "Account deleted!"
    put_user_update = "User updated!"
    post_user_exists = "User exists!"

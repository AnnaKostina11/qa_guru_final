from dataclasses import dataclass
from typing import Optional


@dataclass
class UserCard:
    # Модель платёжной карты.
    # Используется в тестовых данных (например, для UI checkout или для заполнения форм).
    name: str
    number: str
    cvc: str
    expiration_month: str
    expiration_year: str


@dataclass
class User:
    # Модель пользователя для тестовых данных.
    # Используется как источник данных для формирования body в API-запросах (например, /createAccount),
    # а также для повторного использования тех же данных в UI-тестах.
    nick_name: str
    email: str
    password: str
    company_name: str
    country: str
    first_name: str
    last_name: str
    gender: str
    day: str
    month: str
    year: str
    city: str
    state: str
    first_address: str
    second_address: str
    zipcode: str
    mobile_number: str

    # Карта опциональна: не все сценарии требуют платёжные данные.
    card: Optional[UserCard] = None

    def add_card(self, card: UserCard):
        # Упрощённый способ "прикрепить" карту к пользователю в фикстурах.
        self.card = card

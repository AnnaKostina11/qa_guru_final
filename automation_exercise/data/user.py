from dataclasses import dataclass
from typing import Optional

@dataclass
class UserCard:
    name: str
    number: str
    cvc: str
    expiration_month: str
    expiration_year: str

@dataclass
class User:
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
    card: Optional[UserCard] = None

    def add_card(self, card: UserCard):
        self.card = card
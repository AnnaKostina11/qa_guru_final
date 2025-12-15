from enum import Enum


class Country(Enum):
    india = "India"


class Months(Enum):
    may = ("5", "May")


class StatusMessage:
    post_user_created = "User created!"
    del_account_deleted = "Account deleted!"
    put_user_update = "User updated!"
    post_user_exists = "User exists!"
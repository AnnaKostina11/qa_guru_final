import os
from dotenv import load_dotenv

load_dotenv()

SAUCEDEMO_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
SAUCEDEMO_LOGIN = os.getenv("SAUCEDEMO_LOGIN", "standard_user")
SAUCEDEMO_PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")

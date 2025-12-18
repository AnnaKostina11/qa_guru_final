import os
import sys

from pathlib import Path
from dotenv import load_dotenv

def pytest_configure(config):
    env_path = Path(str(config.rootpath)) / ".env"
    load_dotenv(env_path, override=True)

def pytest_sessionstart(session):
    print("\n===== ENV VARIABLES (sorted) =====")
    for k in sorted(os.environ):
        print(f"{k}={os.environ.get(k)}")
    print("===== END ENV =====\n")



sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

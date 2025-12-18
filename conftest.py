import os
import sys

def pytest_sessionstart(session):
    print("\n===== ENV VARIABLES (sorted) =====")
    for k in sorted(os.environ):
        print(f"{k}={os.environ.get(k)}")
    print("===== END ENV =====\n")


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import requests

BASE_URL = "https://www.automationexercise.com/api"

def get_all_brands():
    resp = requests.get(f"{BASE_URL}/brandsList")
    return {
        "status_code": resp.status_code,
        "response": resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {"message": resp.text}
    }

def send_api_request(method, endpoint, **kwargs):
    url = f"{BASE_URL}{endpoint}"
    resp = requests.request(method, url, **kwargs)
    return {
        "status_code": resp.status_code,
        "response": resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {"message": resp.text}
    }
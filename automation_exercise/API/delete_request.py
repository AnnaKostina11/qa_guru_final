from automation_exercise.API.client import send_api_request


def delete_account(email, password):
    return send_api_request("DELETE", "/deleteAccount", data={"email": email, "password": password})

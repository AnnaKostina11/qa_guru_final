from automation_exercise.API.client import send_api_request


def update_user_account(data):
    return send_api_request("PUT", "/updateAccount", data=data)

from automation_exercise.API.client import send_api_request

def post_create_account(user):
    data = {
        "name": user.nick_name,
        "email": user.email,
        "password": user.password,
        "title": "Mr",
        "birth_date": user.day,
        "birth_month": user.month,
        "birth_year": user.year,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "company": user.company_name,
        "address1": user.first_address,
        "address2": user.second_address,
        "country": user.country,
        "zipcode": user.zipcode,
        "city": user.city,
        "state": user.state,
        "mobile_number": user.mobile_number
    }
    return send_api_request("POST", "/createAccount", data=data)

def verify_login(user):
    data = {"email": user.email, "password": user.password}
    return send_api_request("POST", "/verifyLogin", data=data)
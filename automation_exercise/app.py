class PostAPI:
    def create_account(self, user):
        from automation_exercise.API.post_request import post_create_account
        return post_create_account(user)

    def verify_login(self, user):
        from automation_exercise.API.post_request import verify_login
        return verify_login(user)


class DeleteAPI:
    def user_account(self, user):
        from automation_exercise.API.delete_request import delete_account
        return delete_account(user.email, user.password)


class PutAPI:
    def update_user_account(self, data):
        from automation_exercise.API.put_request import update_user_account
        return update_user_account(data)


class GetAPI:
    def all_brand_list(self):
        from automation_exercise.API.client import get_all_brands
        return get_all_brands()


class APIManager:
    def __init__(self):
        self.post = PostAPI()
        self.delete = DeleteAPI()
        self.put = PutAPI()
        self.get = GetAPI()
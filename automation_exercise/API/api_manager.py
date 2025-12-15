from automation_exercise.API.client import APIClient
from automation_exercise.API.delete_request import DeleteAPI
from automation_exercise.API.get_request import GetAPI
from automation_exercise.API.post_request import PostAPI
from automation_exercise.API.put_request import PutAPI


class APIManager:
    # Фасад над набором API-клиентов (GET/POST/PUT/DELETE).
    # Удобно отдавать в фикстуре как единый объект api_application.

    def __init__(self, base_url: str | None = None) -> None:
        # Один общий HTTP client (Session) для всех запросов.
        self.client = APIClient(base_url=base_url)

        # Группировка эндпоинтов по HTTP-методам (как в проекте).
        self.get = GetAPI(self.client)
        self.post = PostAPI(self.client)
        self.put = PutAPI(self.client)
        self.delete = DeleteAPI(self.client)

from automation_exercise.API.client import APIClient


class GetAPI:
    # Группа GET-эндпоинтов.

    def __init__(self, client: APIClient) -> None:
        self.client = client

    def all_brand_list(self) -> dict:
        return self.client.request("GET", "/brandsList")

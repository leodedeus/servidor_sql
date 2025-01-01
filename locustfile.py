from locust import HttpUser, TaskSet, task, between
from itertools import cycle

# Lista de usuários e senhas
user_credentials = [
    {"username": f"user{i}", "password": "password123"}
    for i in range(1, 51)
]
user_cycle = cycle(user_credentials)  # Garante que os usuários sejam usados ciclicamente


class UserBehavior(TaskSet):
    def on_start(self):
        # Pega um par de credenciais
        self.credentials = next(user_cycle)
        # Simula o login
        self.client.post("/accounts/login/", {
            "username": self.credentials["username"],
            "password": self.credentials["password"]
        })

    @task(2)
    def load_home(self):
        self.client.get("/")  # Página inicial

    @task(3)
    def execute_query(self):
        self.client.post("/editor/", {
            "sql_command": "SELECT 1;"
        })


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Simula intervalos entre ações

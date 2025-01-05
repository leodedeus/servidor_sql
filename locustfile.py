from locust import HttpUser, TaskSet, task, between
from itertools import cycle
import re

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

        # Inicializa o token CSRF como None
        self.csrf_token = None

        # Carrega a página inicial para obter o token CSRF
        response = self.client.get("/")
        self.csrf_token = self.extract_csrf_token(response.text)

        if self.csrf_token:
            # Simula o login com o token CSRF
            self.client.post("/accounts/login/", {
                "username": self.credentials["username"],
                "password": self.credentials["password"],
                "csrfmiddlewaretoken": self.csrf_token
            }, headers={"Referer": "/"})
        else:
            print("Erro: Token CSRF não encontrado. Requisições POST podem falhar.")

    @task(2)
    def load_home(self):
        self.client.get("/")  # Página inicial

    @task(3)
    def execute_query(self):
        if self.csrf_token:
            # Envia uma requisição POST para o endpoint `/editor/`
            self.client.post("/editor/", {
                "sql_command": "SELECT 1;",
                "csrfmiddlewaretoken": self.csrf_token
            }, headers={"Referer": "/"})
        else:
            print("Erro: Tentativa de usar CSRF token não definido.")

    def extract_csrf_token(self, response_text):
        """
        Extrai o token CSRF do conteúdo HTML.
        """
        match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response_text)
        return match.group(1) if match else None


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Simula intervalos entre ações


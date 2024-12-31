from django.db import models
from django.contrib.auth.models import User  # Import do modelo User

class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")  # Relacionamento com o usuário
    sql_command = models.TextField("Comando SQL")
    result = models.TextField("Resultado", blank=True, null=True)
    created_at = models.DateTimeField("Data de criação", auto_now_add=True)

    class Meta:
        db_table = 'querys'  # Nome personalizado para a tabela

    def __str__(self):
        return f"Consulta de {self.user.username} em {self.created_at}"



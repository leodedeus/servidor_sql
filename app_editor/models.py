from django.db import models

class Query(models.Model):
    sql_command = models.TextField("Comando SQL")
    result = models.TextField("Resultado", blank=True, null=True)
    created_at = models.DateTimeField("Data de criação", auto_now_add=True)

    class Meta:
        db_table = 'querys'  # Nome personalizado para a tabela

    def __str__(self):
        return f"Consulta em {self.created_at}"


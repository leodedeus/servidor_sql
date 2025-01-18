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

'''
class Censo2022Basico(models.Model):
    codigo_municipio = models.IntegerField(primary_key=True, blank=False, null=False)
    nome_municipio = models.TextField(blank=True, null=True)
    regiao = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    area_km2 = models.FloatField(blank=True, null=True)
    total_pessoas = models.IntegerField(blank=True, null=True)
    total_domicilios = models.IntegerField(blank=True, null=True)
    tot_domicilios_particulares = models.IntegerField(blank=True, null=True)
    tot_domicilios_coletivos = models.IntegerField(blank=True, null=True)
    media_moradores_domicilios_ocupados = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'censo2022_basico'

class Censo2022Demografia(models.Model):
    codigo_municipio = models.IntegerField(primary_key=True, blank=False, null=False)
    total_moradores = models.IntegerField(blank=True, null=True)
    total_sexo_masculino = models.IntegerField(blank=True, null=True)
    total_sexo_feminino = models.IntegerField(blank=True, null=True)
    pessoas_0_4_anos = models.IntegerField(blank=True, null=True)
    pessoas_5_9_anos = models.IntegerField(blank=True, null=True)
    pessoas_10_14_anos = models.IntegerField(blank=True, null=True)
    pessoas_15_19_anos = models.IntegerField(blank=True, null=True)
    pessoas_20_24_anos = models.IntegerField(blank=True, null=True)
    pessoas_25_29_anos = models.IntegerField(blank=True, null=True)
    pessoas_30_39_anos = models.IntegerField(blank=True, null=True)
    pessoas_40_49_anos = models.IntegerField(blank=True, null=True)
    pessoas_50_59_anos = models.IntegerField(blank=True, null=True)
    pessoas_60_69_anos = models.IntegerField(blank=True, null=True)
    pessoas_70_mais_anos = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'censo2022_demografia'

class Test(models.Model):
    name = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
'''
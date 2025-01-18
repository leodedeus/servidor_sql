from django.contrib import admin
from .models import Query

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('sql_command', 'created_at')  # Mostra o comando e a data no admin

'''
@admin.register(Censo2022Basico)
class Censo2022BasicoAdmin(admin.ModelAdmin):
    list_display = ('codigo_municipio', 'nome_municipio')

@admin.register(Censo2022Demografia)
class Censo2022DemografiaAdmin(admin.ModelAdmin):
    list_display = ('codigo_municipio',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
'''
from django.contrib import admin
from .models import Query

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('sql_command', 'created_at')  # Mostra o comando e a data no admin


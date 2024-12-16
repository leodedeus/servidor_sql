from django.urls import path
from . import views

urlpatterns = [
    path('', views.sql_editor, name='sql_editor'),
]

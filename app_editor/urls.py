from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('editor/', views.sql_editor, name='sql_editor'),
    path('accounts/logout/',views.logout_view, name='logout'),
]

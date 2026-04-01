from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_home),
    path("login.agro", views.login_agricultor)
]
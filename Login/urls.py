from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path("", views.login_home, name="login_home"),
    path("login_agro", include([
        path ("", views.login_agricultor, name="login_agricultor"),
        path("criar_agro", views.criar_agricultor, name="criar_agricultor")])),
    path("login_tec", views.login_tecnico, name="login_tecnico"),
]
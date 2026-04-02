from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_home(request):
    return render(request, "login/login_page.html")
def login_agricultor(request):
    return render(request, "login/login_agro.html")
def login_tecnico(request):
    return render(request, "login/login_tec.html")
def criar_agricultor(request):
    return render(request, "login/criar_agro.html")
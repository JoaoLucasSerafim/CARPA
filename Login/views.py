from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_home(request):
    return render(request, "login/login_page.html")
def login_agricultor(request):
    return HttpResponse("Adicione aqui seu login, ou crie uma conta")
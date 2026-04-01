from django.http import HttpResponse
from django.shortcuts import render

def teste_view(request):
    return HttpResponse("<h1>Essa é a Rota de TESTE</h1>")
def index_view(request):
    return render(request, "homepage/homepage.html")
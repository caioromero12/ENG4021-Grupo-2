from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def quemsomos(request):
    return render(request, 'quemsomos.html')

def login_custom(request):
    return render(request, 'login.html')

def moda_sociedade(request):
    return render(request, 'moda_sociedade.html')

def estilos(request):
    return render(request, 'estilos.html')

def comentarios(request):
    return render(request, 'comentarios.html')
    
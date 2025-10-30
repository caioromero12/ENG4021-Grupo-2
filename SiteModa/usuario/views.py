from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Perfil

def login_custom(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos.'})
    return render(request, 'login.html')


def cadastro(request):
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']

        # Cria o usuário
        user = User.objects.create_user(username=email, email=email, password=senha)
        Perfil.objects.create(user=user, nome_completo=nome)

        return redirect('login')
    return render(request, 'cadastro.html')


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def quemsomos(request):
    return render(request, 'quemsomos.html')

@login_required(login_url='login')
def moda_sociedade(request):
    return render(request, 'moda_sociedade.html')

@login_required(login_url='login')
def estilos(request):
    return render(request, 'estilos.html')

@login_required(login_url='login')
def comentarios(request):
    return render(request, 'comentarios.html')


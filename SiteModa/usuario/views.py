from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.utils.decorators import method_decorator
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
        estilo_favorito = request.POST.get('estilo_favorito', '')
        tamanho_roupa = request.POST.get('tamanho_roupa', '')

        # Cria o usuário
        user = User.objects.create_user(username=email, email=email, password=senha)
        # Cria o perfil com os novos campos
        Perfil.objects.create(
            user=user, 
            nome_completo=nome,
            estilo_favorito=estilo_favorito,
            tamanho_roupa=tamanho_roupa
        )

        return redirect('login')
    return render(request, 'cadastro.html')

# PÁGINA DE CONSULTA DE USUÁRIOS
@method_decorator(login_required, name='dispatch')
class ConsultaUsuariosView(View):
    def get(self, request, *args, **kwargs):
        usuarios = Perfil.objects.all().select_related('user')
        contexto = { 'usuarios': usuarios }
        return render(request, 'usuario/consulta_usuarios.html', contexto)

# CONSULTA COM FILTRO
def busca_usuario(request):
    """Página de busca - formulário"""
    return render(request, 'usuario/busca_usuario.html')

def resultado_busca(request):
    """Resultado da busca com filtros"""
    estilo_busca = request.GET.get('estilo', '')
    tamanho_busca = request.GET.get('tamanho', '')
    
    # Começa com todos os usuários
    usuarios = Perfil.objects.all().select_related('user')
    
    # Aplica filtros se foram preenchidos
    if estilo_busca:
        usuarios = usuarios.filter(estilo_favorito__icontains=estilo_busca)
    if tamanho_busca:
        usuarios = usuarios.filter(tamanho_roupa__icontains=tamanho_busca)
    
    contexto = {
        'usuarios': usuarios,
        'estilo_buscado': estilo_busca,
        'tamanho_buscado': tamanho_busca
    }
    return render(request, 'usuario/resultado_busca.html', contexto)

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
    

    
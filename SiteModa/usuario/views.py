from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from .models import Perfil
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import UnifiedFashionStyle
import json

logger = logging.getLogger(__name__)

@csrf_exempt
def login_custom(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Permitir autenticação usando email ou username: se o usuário
        # enviar um email, buscar o username correspondente.
        username_to_auth = username
        if '@' in username:
            try:
                user_obj = User.objects.filter(email__iexact=username).first()
                if user_obj:
                    username_to_auth = user_obj.username
            except Exception:
                # qualquer erro aqui deixamos username como veio
                username_to_auth = username

        # Log de depuração (NÃO logar a senha)
        logger.info(f"Login attempt: form_username={username}, username_to_auth={username_to_auth}")
        try:
            user = authenticate(request, username=username_to_auth, password=password)
            logger.info(f"Authentication result for {username_to_auth}: {'SUCCESS' if user is not None else 'FAIL'}")
        except Exception as e:
            logger.exception('Error during authenticate')
            user = None

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

        user = User.objects.create_user(username=email, email=email, password=senha)

        Perfil.objects.create(
            user=user, 
            nome_completo=nome,
            estilo_favorito=estilo_favorito,
            tamanho_roupa=tamanho_roupa
        )

        return redirect('login')
    return render(request, 'cadastro.html')


@method_decorator(login_required, name='dispatch')
class ConsultaUsuariosView(View):
    def get(self, request, *args, **kwargs):
        usuarios = Perfil.objects.all().select_related('user')
        contexto = { 'usuarios': usuarios }
        return render(request, 'usuario/consulta_usuarios.html', contexto)


def busca_usuario(request):
    return render(request, 'usuario/busca_usuario.html')


def resultado_busca(request):
    estilo_busca = request.GET.get('estilo', '')
    tamanho_busca = request.GET.get('tamanho', '')
    
    usuarios = Perfil.objects.all().select_related('user')
    
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

@login_required(login_url='login')
def lojas_parceiras(request):
    return render(request, 'lojas_parceiras.html')

@login_required(login_url='login')
def timeline(request):
    return render(request, 'timeline.html')

@login_required(login_url='login')
def consultoria(request):
    return render(request, 'consultoria.html')

@login_required(login_url='login')
def atendimento(request):
    return render(request, 'atendimento.html')

@login_required(login_url='login')
def formulario(request):
    return render(request, 'formulario.html')

@login_required(login_url='login')
def novidades(request):
    return render(request, 'novidades.html')

@login_required(login_url='login')
def country(request):
    return render(request, 'country.html')

@login_required(login_url='login')
def nossosProdutosBoho(request):
    return render(request, 'nossosProdutosBoho.html')

@login_required(login_url='login')
def nossosProdutosOutfitStreet(request):
    return render(request, 'nossosProdutosOutfitStreet.html')


def parceiros(request):
    """View para página Como se Tornar Afiliado"""
    return render(request, 'parceiros.html')

@login_required(login_url='login')
def homeprodutos(request):
    tamanho = request.GET.get('tamanho', '')

    produtos = [
        {"nome": "Bota Country", "tamanhos": ["P", "M", "G"], "img": "img/country/bota-country.jpg"},
        {"nome": "Camisa Xadrez", "tamanhos": ["M", "G"], "img": "img/country/camisa-xadrez.jpg"},
        {"nome": "Jeans Bootcut", "tamanhos": ["G"], "img": "img/country/jeans-retro.jpg"},
        {"nome": "Colete de Couro", "tamanhos": ["P", "M"], "img": "img/country/colete-couro.jpg"},
    ]

    # Filtra pela seleção do usuário
    if tamanho:
        produtos = [p for p in produtos if tamanho in p["tamanhos"]]

    contexto = {
        "produtos": produtos,
        "tamanho_selecionado": tamanho,
    }

    return render(request, 'homeprodutos.html', contexto)

@login_required(login_url='login')
def modaretro(request):
    return render(request, 'modaretro.html')

def estilos_busca(request):
    return render(request, "estilos_busca.html")


def estilos_resposta(request):
    q = request.GET.get("q", "").strip()

    if q:
        styles = UnifiedFashionStyle.objects.filter(name__icontains=q)
    else:
        styles = UnifiedFashionStyle.objects.all()

    return render(request, "estilos_resposta.html", {
        "styles": styles,
        "query": q
    })


def style_detail(request, slug):
    style = get_object_or_404(UnifiedFashionStyle, slug=slug)
    return render(request, "styles/detail.html", {"style": style})


def place_order(request, slug):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    style = get_object_or_404(UnifiedFashionStyle, slug=slug)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    buyer = payload.get("buyer")
    items = payload.get("items")
    status = payload.get("status", "PENDING")

    if not buyer or not buyer.get("email"):
        return JsonResponse({"error": "Email é obrigatório"}, status=400)

    try:
        order = style.place_order(buyer, items, status)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "order_id": order["order_id"],
        "total": order["total"]
    })
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('quemsomos/', views.quemsomos, name='quemsomos'),
    path('moda-sociedade/', views.moda_sociedade, name='moda_sociedade'),
    path('estilos/', views.estilos, name='estilos'),
    path('comentarios/', views.comentarios, name='comentarios'),

    # Páginas
    path('lojas-parceiras/', views.lojas_parceiras, name='lojas_parceiras'),
    path('timeline/', views.timeline, name='timeline'),

    # NOVAS PÁGINAS
    path('consultoria/', views.consultoria, name='consultoria'),
    path('atendimento/', views.atendimento, name='atendimento'),
    path('formulario/', views.formulario, name='formulario'),
    path('homeprodutos/', views.homeprodutos, name='homeprodutos'),
    path('country/', views.country, name='country'),
    path('modaretro/', views.modaretro, name='modaretro'),

    # NOVIDADES / PARCEIROS
    path('novidades/', views.novidades, name='novidades'),
    path('parceiros/', views.parceiros, name='parceiros'),

    # Autenticação
    path('login/', views.login_custom, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # Consulta de usuários
    path('consulta/', views.ConsultaUsuariosView.as_view(), name='consulta_usuarios'),

    # Busca com filtro (usuários)
    path('buscar/', views.busca_usuario, name='busca_usuario'),
    path('resultado-busca/', views.resultado_busca, name='resultado_busca'),

    # PÁGINAS DE PRODUTOS (fixas)
    path('nossos-produtos-boho/', views.nossosProdutosBoho, name='nossosProdutosBoho'),
    path('nossos-produtos-street/', views.nossosProdutosOutfitStreet, name='nossosProdutosOutfitStreet'),

    # --- INCLUSÃO das rotas de ESTILOS (arquivo dedicado) ---
    path('styles/', include('usuario.estilos_urls', namespace='styles')),
]

# Servir media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
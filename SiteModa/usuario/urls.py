from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quemsomos/', views.quemsomos, name='quemsomos'),
    path('moda-sociedade/', views.moda_sociedade, name='moda_sociedade'),
    path('estilos/', views.estilos, name='estilos'),
    path('comentarios/', views.comentarios, name='comentarios'),

    # Páginas adicionadas pelas duas versões
    path('lojas-parceiras/', views.lojas_parceiras, name='lojas_parceiras'),
    path('timeline/', views.timeline, name='timeline'),

    # NOVAS PÁGINAS
    path('consultoria/', views.consultoria, name='consultoria'),
    path('atendimento/', views.atendimento, name='atendimento'),
    path('formulario/', views.formulario, name='formulario'),

    # Autenticação
    path('login/', views.login_custom, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # Consulta de usuários
    path('consulta/', views.ConsultaUsuariosView.as_view(), name='consulta_usuarios'),

    # Busca com filtro
    path('buscar/', views.busca_usuario, name='busca_usuario'),
    path('resultado-busca/', views.resultado_busca, name='resultado_busca'),
]

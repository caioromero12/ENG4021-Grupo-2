from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quemsomos/', views.quemsomos, name='quemsomos'),
    path('moda-sociedade/', views.moda_sociedade, name='moda_sociedade'),
    path('estilos/', views.estilos, name='estilos'),
    path('comentarios/', views.comentarios, name='comentarios'),
    path('lojas-parceiras/', views.lojas_parceiras, name='lojas_parceiras'),


    # Rotas de autenticação
    path('login/', views.login_custom, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # Página de consulta
    path('consulta/', views.ConsultaUsuariosView.as_view(), name='consulta_usuarios'),
    
    # NOVAS ROTAS: Consulta com filtro
    path('buscar/', views.busca_usuario, name='busca_usuario'),
    path('resultado-busca/', views.resultado_busca, name='resultado_busca'),
]


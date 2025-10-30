from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quemsomos/', views.quemsomos, name='quemsomos'),
    path('moda-sociedade/', views.moda_sociedade, name='moda_sociedade'),
    path('estilos/', views.estilos, name='estilos'),
    path('comentarios/', views.comentarios, name='comentarios'),

    # Rotas de autenticação
    path('login/', views.login_custom, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
]

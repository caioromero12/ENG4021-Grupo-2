from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quemsomos/', views.quemsomos, name='quemsomos'),
    path('login/', views.login_custom, name='login'),
    path('moda-sociedade/', views.moda_sociedade, name='moda_sociedade'),
    path('estilos/', views.estilos, name='estilos'),
    path('comentarios/', views.comentarios, name='comentarios'),
]


from django.urls import path
from . import views

app_name = "styles"

urlpatterns = [
    path("buscar/", views.estilos_busca, name="busca"),
    path("resultado/", views.estilos_resposta, name="resposta"),
    path("<slug:slug>/", views.style_detail, name="detail"),
    path("<slug:slug>/order/", views.place_order, name="place_order"),
]
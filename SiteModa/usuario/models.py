from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    estilo_favorito = models.CharField(max_length=50, blank=True)  # NOVO CAMPO
    tamanho_roupa = models.CharField(max_length=10, blank=True)   # NOVO CAMPO

    def __str__(self):
        return self.nome_completo
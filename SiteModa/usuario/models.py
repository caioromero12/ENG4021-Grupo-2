from django.db import models
from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.text import slugify
from django.utils import timezone
import uuid

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    estilo_favorito = models.CharField(max_length=50, blank=True)  # NOVO CAMPO
    tamanho_roupa = models.CharField(max_length=10, blank=True)   # NOVO CAMPO

    def __str__(self):
        return self.nome_completo

class UnifiedFashionStyle(models.Model):
    """
    Modelo único que concentra:
    - informações do estilo (nome, descrição, história)
    - países onde é popular (lista)
    - celebridades que usam o estilo (lista de objetos)
    - produtos/peças (cada produto tem tamanhos, preço por tamanho e estoque)
    - pedidos básicos registrados no próprio objeto (lista de orders)
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_column='NAME')
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_column='SLUG')
    short_description = models.CharField(max_length=512, blank=True, db_column='SHORT_DESC')
    history = models.TextField(blank=True, db_column='HISTORY')

    # JSON fields (listas de dicionários ou strings)
    countries = models.JSONField(default=list, blank=True, db_column='COUNTRIES')
    # celebridades: lista de dicts, por exemplo: {"name":"Zendaya","image_url":"...","social":"..."}
    celebrities = models.JSONField(default=list, blank=True, db_column='CELEBRITIES')

    # products: lista de dicts com estrutura prevista abaixo
    # Exemplo de produto:
    # {
    #   "product_id": "p1",
    #   "name": "Jaqueta X",
    #   "sku": "JX-001",
    #   "images": ["url1","url2"],
    #   "sizes": [
    #       {"label":"S","price":249.90,"stock":5},
    #       {"label":"M","price":249.90,"stock":2}
    #   ],
    #   "active": True
    # }
    products = models.JSONField(default=list, blank=True, db_column='PRODUCTS')

    # orders: lista de pedidos (cada pedido é um dict)
    # Exemplo:
    # {
    #   "order_id":"uuid",
    #   "buyer":{"name":"Caio","email":"caio@example.com"},
    #   "items":[{"product_id":"p1","size":"M","quantity":1,"unit_price":249.90}],
    #   "total":249.90,
    #   "status":"PAID",
    #   "created_at":"2025-12-07T21:00:00Z"
    # }
    orders = models.JSONField(default=list, blank=True, db_column='ORDERS')

    featured = models.BooleanField(default=False, db_column='FEATURED')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    updated_at = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        managed = True
        db_table = 'UnifiedFashionStyle'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or str(uuid.uuid4())[:8]
            # garante unicidade simples
            slug = base
            counter = 1
            while UnifiedFashionStyle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    # ---------- helpers para manipular products/orders ----------
    def get_product(self, product_id):
        """Retorna o dicionário do produto ou None."""
        for p in self.products:
            if p.get("product_id") == product_id:
                return p
        return None

    def update_product(self, product_id, new_product_dict):
        """Substitui o produto com product_id pelo novo dict (e salva)."""
        updated = False
        for i, p in enumerate(self.products):
            if p.get("product_id") == product_id:
                self.products[i] = new_product_dict
                updated = True
                break
        if updated:
            self.save()
        return updated

    def place_order(self, buyer: dict, items: list, status: str = "PENDING"):
        """
        buyer: dict com pelo menos {"name":..,"email":..} (pode ter mais campos)
        items: lista de dicts: [{"product_id":"p1","size":"M","quantity":1}, ...]
        Retorna: dict do pedido criado em caso de sucesso.
        Lança ValueError em caso de erro (estoque insuficiente, produto não encontrado, etc).
        """
        if not items:
            raise ValueError("Nenhum item informado para o pedido.")

        # vamos operar dentro de uma transação para evitar inconsistência
        with transaction.atomic():
            # copiar produtos localmente para modificar
            prod_list = self.products.copy()
            total = 0.0
            # preparações para checagem e atualização
            for it in items:
                pid = it.get("product_id")
                size_label = it.get("size")
                qty = int(it.get("quantity", 1))
                if qty <= 0:
                    raise ValueError("Quantidade deve ser >= 1.")

                # encontrar produto
                prod = None
                for p in prod_list:
                    if p.get("product_id") == pid and p.get("active", True):
                        prod = p
                        break
                if prod is None:
                    raise ValueError(f"Produto {pid} não encontrado ou inativo.")

                # encontrar tamanho
                size_found = None
                for s in prod.get("sizes", []):
                    if s.get("label") == size_label:
                        size_found = s
                        break
                if size_found is None:
                    raise ValueError(f"Tamanho {size_label} não disponível para produto {pid}.")

                # checar estoque
                stock = int(size_found.get("stock", 0))
                if stock < qty:
                    raise ValueError(f"Estoque insuficiente para {prod.get('name')} tamanho {size_label} (disponível {stock}).")

                # calcular preço
                price = float(size_found.get("price", 0.0))
                total += price * qty

                # decrementar estoque (na cópia)
                size_found["stock"] = stock - qty

            # tudo ok -> criar order
            order_id = uuid.uuid4().hex
            order = {
                "order_id": order_id,
                "buyer": buyer,
                "items": [],
                "total": round(total, 2),
                "status": status,
                "created_at": timezone.now().isoformat()
            }

            # preenche itens com unit_price e confirma alterações na lista de produtos
            for it in items:
                pid = it.get("product_id")
                size_label = it.get("size")
                qty = int(it.get("quantity", 1))
                # localizar produto atualizado na prod_list
                prod = next((p for p in prod_list if p.get("product_id") == pid), None)
                size_found = next((s for s in prod.get("sizes", []) if s.get("label") == size_label), None)
                unit_price = float(size_found.get("price", 0.0))
                order["items"].append({
                    "product_id": pid,
                    "product_name": prod.get("name"),
                    "size": size_label,
                    "quantity": qty,
                    "unit_price": round(unit_price, 2)
                })

            # grava alterações: substituir products pela prod_list atualizada e adicionar order
            self.products = prod_list
            # insere o pedido no início da lista (mais recente primeiro)
            current_orders = self.orders or []
            current_orders.insert(0, order)
            self.orders = current_orders
            self.save()

            return order

    # utilitário rápido para adicionar produto (programaticamente)
    def add_product(self, product_dict):
        """
        product_dict deve ter pelo menos:
        {
          "product_id": "p1",
          "name":"Blusa X",
          "sizes":[{"label":"S","price":199.9,"stock":10}, ...],
          "active": True
        }
        """
        if not product_dict.get("product_id"):
            product_dict["product_id"] = uuid.uuid4().hex[:8]
        self.products.append(product_dict)
        self.save()
        return product_dict["product_id"]
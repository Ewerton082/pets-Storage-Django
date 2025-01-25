from django.db import models
from django.contrib.auth.models import User

# Create your models here.

WEIGHTS_FOODS = (
    ("10.1", "10 KG"),
    ("15.1", "15 KG"),
    ("20.1", "20 KG"),
    ("25.1", "25 KG"),
)

ANIMALS_TYPE = (
    ("Cão", "Cachorro"),
    ("Gato", "Gato"),
)


class Brands(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, verbose_name="Id")
    name = models.CharField(blank=False, null=False, max_length=70, verbose_name="Nome da Empresa")
    corporate = models.CharField(blank=True, null=True, max_length=30, verbose_name="Razão Social")
    seller = models.CharField(blank=True, null=True, max_length=80, verbose_name="Nome do Vendedor")

    def __str__(self):
        return self.name


class StorageFoods(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, verbose_name="Id")
    brand = models.ForeignKey(to=Brands, on_delete=models.CASCADE, verbose_name="Nome da Marca", related_name="brand_of_food")
    food = models.CharField(blank=False, null=False, max_length=150, verbose_name="Nome da ração")
    weight = models.CharField(choices=WEIGHTS_FOODS, max_length=5, blank=False, null=False, verbose_name="Peso da ração")
    quantity = models.IntegerField(blank=False, null=False, verbose_name="Quantidade")
    alert_quantity = models.IntegerField(blank=True, null=True, verbose_name="Quantidade de Alerta")
    animal = models.CharField(choices=ANIMALS_TYPE, blank=False, null=False, max_length=6, verbose_name="Animal")
    buy_price = models.FloatField(blank=True, null=True, verbose_name="Valor de compra")
    sell_price_card = models.FloatField(blank=True, null=True, verbose_name="Valor de venda cartão")
    sell_price_money = models.FloatField(blank=True, null=True, verbose_name="Valor de venda dinheiro")
    image = models.ImageField(upload_to="foods/", blank=True, null=True)

    def __str__(self):
        return self.food + " " + self.weight


class StorageMoviments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    food = models.ForeignKey(StorageFoods, on_delete=models.CASCADE, verbose_name="Ração")
    moviment_type = models.CharField(max_length=6, verbose_name="Ação")
    quantity = models.IntegerField(verbose_name="Quantidade")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Data da operação")

    def __str__(self):
        return f"{self.user} - {self.food} ({self.moviment_type}) - {self.quantity}"


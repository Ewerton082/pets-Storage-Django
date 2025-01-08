# Generated by Django 5.1.4 on 2025-01-08 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=70, verbose_name='Nome da Empresa')),
                ('corporate', models.CharField(blank=True, max_length=30, null=True, verbose_name='Razão Social')),
            ],
        ),
        migrations.CreateModel(
            name='StorageFoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('food', models.CharField(max_length=150, verbose_name='Nome da ração')),
                ('weight', models.CharField(choices=[(10.1, '10 KG'), (15.1, '15 KG'), (20.1, '20 KG'), (25.1, '25 KG')], max_length=5, verbose_name='Peso da ração')),
                ('quantity', models.IntegerField(verbose_name='Quantidade')),
                ('animal', models.CharField(choices=[('Cão', 'Cachorro'), ('Gato', 'Gato')], max_length=6, verbose_name='Animal')),
                ('buy_price', models.FloatField(blank=True, null=True, verbose_name='Valor de compra')),
                ('sell_price_card', models.FloatField(blank=True, null=True, verbose_name='Valor de venda cartão')),
                ('sell_price_money', models.FloatField(blank=True, null=True, verbose_name='Valor de venda dinheiro')),
                ('image', models.ImageField(blank=True, null=True, upload_to='foods/')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_of_food', to='storage.brands', verbose_name='Nome da Marca')),
            ],
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-20 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_brands_seller'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageMoviments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moviment_type', models.CharField(max_length=10, verbose_name='Ação')),
                ('quantity', models.IntegerField(verbose_name='Quantidade')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Data da operação')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.storagefoods', verbose_name='Ração')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
    ]
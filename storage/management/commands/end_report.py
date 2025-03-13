from django.core.management import BaseCommand
from storage.models import StorageMonthlyReport, StorageFoods
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Este comando Cria o Relatorio Mensal de todas as rações que temos para que no final da semana tenhamos estatisticas"

    def handle(self, *args, **options):
        today = timezone.now().date()
        last_monday = today - timedelta(days=today.weekday())

        products = StorageMonthlyReport.objects.filter(report_date=last_monday)

        for item in products:
            food = item.select_food

            item.ending_quantity = food.quantity
            item.save()

            self.stdout.write(self.style.ERROR(f" Relatório finalizado com sucesso para {food.food}"))
           
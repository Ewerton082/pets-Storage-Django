from django.core.management import BaseCommand
from storage.models import StorageMonthlyReport, StorageFoods
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Este comando Cria o Relatorio Mensal de todas as rações que temos para que no final da semana tenhamos estatisticas"

    def handle(self, *args, **options):
        today = timezone.now().date()
        last_monday = today - timedelta(days=today.weekday())

        products = StorageFoods.objects.all()

        for item in products:
            report, created = StorageMonthlyReport.objects.get_or_create(
                report_date = last_monday,
                select_food = item,
                defaults={
                    "starter_quantity": item.quantity
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Relatorio Criado com sucesso para {item.food}"))
            else:
                self.stdout.write(self.style.WARNING(f"Ja Existia um relatorio para {item.food}"))

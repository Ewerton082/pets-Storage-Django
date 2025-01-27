from django.core.management import BaseCommand
from storage.models import Brands, StorageFoods
import csv


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('href', help="Escreva o diretorio do arquivo CSV")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["href"]

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:

                    brand = row.get("brand", "").strip()
                    brand = Brands.objects.filter(name=brand).first()
                    if not brand:
                        self.stdout.write(self.style.ERROR(f"Não encontramos a marca então não adicionamos a {name}"))
                        continue
                    
                    name = row.get("name", "").strip()
                    weight = row.get("weight", "").strip()
                    quantity = row.get("quantity", "").strip()
                    quantity_alert = row.get("quantity_alert", "").strip()
                    animal = row.get("animal", "").strip()
                    buy = row.get("buy", "").strip()
                    sell_cred = row.get("sell_cred", "").strip()
                    sell_money = row.get("sell_money", "").strip()

                    
                    self.stdout.write(self.style.NOTICE(f"{name} Cadastrado com sucesso"))

                self.stdout.write(self.style.SUCCESS("Importação concluida."))

        except FileNotFoundError:
            return self.stdout.write(self.style.ERROR("Não foi passado nenhum arquivo"))

        except Exception as error:
            return self.stdout.write(self.style.ERROR(error))
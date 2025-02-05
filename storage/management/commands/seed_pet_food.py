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

                    brand_seed = row.get("brand", "").strip()
                    name_seed = row.get("name", "").strip()
                    brand_seed = Brands.objects.filter(name=brand_seed).first()
                    if not brand_seed:
                        self.stdout.write(self.style.ERROR(f"Não encontramos a marca então não adicionamos a {name_seed}"))
                        continue

                    weight_seed = row.get("weight", "").strip()
                    quantity_seed = row.get("quantity", "").strip()
                    quantity_alert_seed = row.get("quantity_alert", "").strip()
                    animal_seed = row.get("animal", "").strip()
                    buy_seed = row.get("buy", "").strip()
                    sell_cred_seed = row.get("sell_cred", "").strip()
                    sell_money_seed = row.get("sell_money", "").strip()

                    StorageFoods.objects.create(
                        brand=brand_seed,
                        food=name_seed,
                        weight=weight_seed,
                        quantity=quantity_seed,
                        alert_quantity=quantity_alert_seed,
                        animal=animal_seed,
                        buy_price=buy_seed,
                        sell_price_card=sell_cred_seed,
                        sell_price_money=sell_money_seed
                    )

                    self.stdout.write(self.style.NOTICE(f"{name_seed} Cadastrado com sucesso"))

                self.stdout.write(self.style.SUCCESS("Importação concluida."))

        except FileNotFoundError:
            return self.stdout.write(self.style.ERROR("Não foi passado nenhum arquivo"))

        except Exception as error:
            return self.stdout.write(self.style.ERROR(error))

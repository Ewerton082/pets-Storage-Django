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
                    brand_bd = Brands.objects.filter(name=brand_seed).first()
                    if not brand_bd:
                        self.stdout.write(self.style.ERROR(f"Não encontramos a marca {brand_bd} então não adicionamos a {name_seed}"))
                        continue

                    weight_seed = float(row.get("weight", 0) or 0)
                    quantity_seed = int(row.get("quantity", 0) or 0)
                    quantity_alert_seed = int(row.get("quantity_alert", 0) or 0)
                    animal_seed = row.get("animal", None).strip()
                    buy_seed = float(row.get("buy", 0) or 0)
                    sell_cred_seed = float(row.get("sell_cred", 0) or 0)
                    sell_money_seed = float(row.get("sell_money", 0) or 0)

                    obj, created = StorageFoods.objects.get_or_create(food=name_seed,
                                                                      weight=weight_seed,
                                                        defaults={
                                                            "brand": brand_bd,
                                                            "animal": animal_seed,
                                                            "quantity": quantity_seed,
                                                            "alert_quantity": quantity_alert_seed,
                                                            "buy_price": buy_seed,
                                                            "sell_price_card": sell_cred_seed,
                                                            "sell_price_money": sell_money_seed,
                                                        })


                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Ração '{name_seed}' (Peso: {weight_seed}kg) criada!"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Ração '{name_seed}' já existia no banco de dados."))
                    

                self.stdout.write(self.style.SUCCESS("Importação concluida."))

        except FileNotFoundError:
            return self.stdout.write(self.style.ERROR("Não foi passado nenhum arquivo"))

        except Exception as error:
            return self.stdout.write(self.style.ERROR(error))

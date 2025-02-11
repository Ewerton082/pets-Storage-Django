from django.core.management import BaseCommand
from storage.models import Brands
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
                    brand_name = row.get("name", "").strip()
                    brand_id = row.get("id", "").strip()
                    brand_seller = row.get("seller", "").strip()
                    brand_seller_tel = row.get("phone", "").strip()
                    Brands.objects.create(
                        name=brand_name,
                        corporate=brand_id,
                        seller=brand_seller,
                        contact_seller=brand_seller_tel,
                    )

                    self.stdout.write(self.style.WARNING(f"{self.style.SQL_KEYWORD(brand_name)} Cadastrado com sucesso"))

                self.stdout.write(self.style.SUCCESS("Importação concluida."))

        except FileNotFoundError:
            return self.stdout.write(self.style.ERROR("Não foi passado nenhum arquivo"))

        except Exception as error:
            return self.stdout.write(self.style.ERROR(error))

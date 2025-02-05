from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from storage.models import Brands, StorageFoods


class ViewHomeTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username="AdminTest", password="AdminPass")

    def test_home_status_200(self):
        self.client.login(username="AdminTest", password="AdminPass")

        url = reverse("storage:Home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ViewsFoodTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username="AdminTest", password="AdminPass")
        self.brand = Brands.objects.create(name="BrandTest")
        self.food = StorageFoods.objects.create(
            brand=self.brand,
            food="Ração Teste",
            weight="25.1",
            quantity=10,
            alert_quantity=5,
            animal="Cão",
            buy_price=20.0,
            sell_price_card=30.0,
            sell_price_money=28.0,
            image=""
        )

    def test_create_foods(self):

        url = reverse("storage:Create")

        data = {
            'brand': self.brand.id,
            'food': 'Ração Teste',
            'weight': '25.1',
            'quantity': 1,
            'alert_quantity': 5,
            'animal': 'Cão',
            'buy_price': 20.0,
            'sell_price_card': 30.0,
            'sell_price_money': 28.0,
            'image': ''
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.client.login(username="AdminTest", password="AdminPass")
        self.assertRedirects(response, reverse("storage:Home"))

    def test_food_detail(self):
        self.client.login(username="AdminTest", password="AdminPass")

        url = reverse("storage:Detail", kwargs={"pk": self.food.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.food.food)
        self.assertContains(response, self.food.brand.name)
        self.assertContains(response, self.food.weight)
        self.assertContains(response, str(self.food.quantity))
        self.assertContains(response, str(self.food.alert_quantity))
        self.assertContains(response, self.food.image.url if self.food.image else "")

    def test_update_foods(self):
        self.client.login(username="AdminTest", password="AdminPass")

        url = reverse("storage:Update", kwargs={"pk": self.food.pk})

        data = {
            'brand': self.brand.id,
            'food': 'Ração Atualizada',
            'weight': '15.1',
            'quantity': 35,
            'alert_quantity': 10,
            'animal': 'Gato',
            'buy_price': 99.5,
            'sell_price_card': 149.6,
            'sell_price_money': 133.0,
            'image': ''
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse("storage:Detail", kwargs={"pk": self.food.pk}))

        updated_food = StorageFoods.objects.get(pk=self.food.pk)
        self.assertEqual(updated_food.food, 'Ração Atualizada')
        self.assertEqual(updated_food.weight, '15.1')
        self.assertEqual(updated_food.quantity, 35)
        self.assertEqual(updated_food.buy_price, 99.5)
        self.assertEqual(updated_food.sell_price_card, 149.6)
        self.assertEqual(updated_food.sell_price_money, 133.0)

    def test_delete_food(self):
        self.client.login(username="AdminTest", password="AdminPass")

        url = reverse("storage:Delete", kwargs={"pk": self.food.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        with self.assertRaises(StorageFoods.DoesNotExist):
            StorageFoods.objects.get(pk=self.food.pk)
        self.assertRedirects(response, reverse("storage:Home"))


class ViewsBrandTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='AdminTest', password='AdminPass')
        self.brand = Brands.objects.create(
            name='PetFood Ltda.',
            corporate='12.345.678/0001-99',
            seller='José Silva'
        )

    def test_create_brand(self):
        self.client.login(username="AdminTest", password="AdminPass")
        url = reverse("storage:CreateBrand")

        data = {
            "name": "Pet Planet",
            "corporate": "98.765.432/1000-77",
            "seller": "Daniel Bastos"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse("storage:Home"))

import datetime
import random

from django.core.management import BaseCommand

from mainapp.models import *


class Command(BaseCommand):
    help = "Generating fake clients, products and purchases"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Client.objects.all().delete()
        Order.objects.all().delete()
        City.objects.all().delete()

        print("!!!", "Generating categories")
        cat_milk = Category.objects.create(name="Молочные продукты")
        cat_meat = Category.objects.create(name="Мясные продукты")
        cat_grains = Category.objects.create(name="Крупы")
        cat_alcohol = Category.objects.create(name="Алкоголь")
        for parent_category, category in [
            (cat_milk, "Сырки"),
            (cat_milk, "Молоко"),
            (cat_milk, "Сыр"),
            (cat_meat, "Колбаса"),
            (cat_meat,"Мясо"),
            (cat_grains,"Просо"),
            (cat_grains, "Рис"),
            (cat_alcohol, "Пиво"),
            (cat_alcohol, "Вино"),
            (cat_alcohol, "Крепкие напитки"),
        ]:
            Category.objects.create(
                name=category,
                parent_category=parent_category,
                is_adult=parent_category == cat_alcohol,
            )

        print("!!!", "Generating products")
        for category in Category.objects.all():
            for i in range(5):
                Product.objects.create(
                    name=f"{category.name}_{i}",
                    price=random.randint(100, 10000),
                    category=category
                )

        print("!!!", "Generating clients")
        for city in ["Almaty", "Shymkent", "Astana"]:
            City.objects.create(name=city)

        cities = list(City.objects.all())
        for i in range(10):
            Client.objects.create(
                name=f"Client_{i}",
                age=random.randint(15, 50),
                city=random.choice(cities)
            )

        print("!!!", "Generating orders")
        clients = list(Client.objects.all())
        products = list(Product.objects.all())
        for _ in range(500):
            product = random.choice(products)
            dt = datetime.datetime(2021, 1, 1) + datetime.timedelta(seconds=random.randint(0, 365*24*60*60))
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            Order.objects.create(
                client=random.choice(clients),
                product=product,
                datetime=dt,
                price=product.price,
                review=random.randint(1, 10),
            )

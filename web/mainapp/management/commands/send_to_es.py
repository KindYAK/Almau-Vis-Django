import datetime
import random

from django.core.management import BaseCommand
from elasticsearch.helpers import parallel_bulk

from AlmauVis.settings import ES_CLIENT
from mainapp.models import *


class Command(BaseCommand):
    help = "Generating fake clients, products and purchases"

    @staticmethod
    def gen_data():
        for order in Order.objects.all():
            yield {
                "_index": "orders",
                "client_name": order.client.name,
                "client_age": order.client.age,
                "client_city": order.client.city.name,
                "product_name": order.product.name,
                "product_price": order.product.price,
                "product_category": order.product.category.name,
                "datetime": order.datetime,
                "price": order.price,
                "review": order.review,
            }

    def handle(self, *args, **options):
        # try:
        #     ES_CLIENT.indices.create("mywords", ignore=True)
        # except:
        #     pass
        for i, (success, info) in enumerate(parallel_bulk(
            ES_CLIENT,
            self.gen_data(),
            thread_count=3,
            chunk_size=10
        )):
            if i % 1000 == 0:
                print(success, info)

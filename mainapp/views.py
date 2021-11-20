import datetime
import os
import random

import pandas as pd
import seaborn as sns

from django.db.models import Count, Avg
from django.views.generic import ListView

from AlmauVis.settings import MEDIA_ROOT, MEDIA_URL
from mainapp.models import *


class OrderListView(ListView):
    template_name = "order_list.html"
    model = Order
    queryset = Order.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['len_clients'] = Client.objects.count()
        qs = Category.objects.filter(product__order__in=self.get_queryset())
        qs = qs.annotate(
            order_count=Count('product__order'),
            average_price=Avg('product__order__price')
        )

        plot = sns.barplot(data=pd.DataFrame([
            {
                "name": i.name,
                "order_count": i.order_count
            } for i in qs
        ]), x="name", y="order_count")

        filename = f"bar-plot-order-count-{str(datetime.datetime.now()).replace(':', '-')}-{random.randint(1, 100000)}.jpg"
        path = os.path.join(
            MEDIA_ROOT,
            filename
        )
        plot.get_figure().savefig(path)
        context['filename'] = MEDIA_URL + "/" + filename
        return context

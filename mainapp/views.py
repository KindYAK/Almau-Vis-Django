import datetime
import os
import random
import time

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

        filename = f"bar-plot-order-count-{str(dict(self.request.GET)).replace(':', '=').replace('<', '(').replace('>', ')')}.jpg"
        path = os.path.join(
            MEDIA_ROOT,
            filename
        )
        context['filename'] = MEDIA_URL + "/" + filename

        try:
            cr = datetime.datetime.fromtimestamp(
                os.path.getmtime(path)
            )
            file_age = (datetime.datetime.now() - cr).seconds
        except:
            file_age = 100 * 60 * 24

        if file_age > 1:
            qs = Category.objects.filter(product__order__in=self.get_queryset())
            qs = qs.annotate(
                order_count=Count('product__order'),
                average_price=Avg('product__order__price')
            )

            plot = sns.barplot(data=pd.DataFrame([
                {
                    "name": i.name,
                    "order_count": i.average_price
                } for i in qs
            ]), x="name", y="order_count")
            plot.get_figure().savefig(path)
        return context

import datetime
import os

import pandas as pd
import seaborn as sns

from django.db.models import Count, Avg
from django.http import JsonResponse
from django.views.generic import ListView

from AlmauVis.settings import MEDIA_ROOT, MEDIA_URL, ES_CLIENT
from mainapp.models import *


def get_order_plot_data(request):
    qs = Category.objects.exclude(parent_category=None)
    qs = qs.annotate(
        order_count=Count('product__order'),
        average_price=Avg('product__order__price')
    )
    df = pd.DataFrame([
        {
            "name": i.name,
            "order_count": i.average_price
        } for i in qs
    ]
    )
    return JsonResponse(
        {
            "category_names": list(df.name),
            "category_values": list(df.order_count)
        }
    )


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

        qs = Category.objects.filter(product__order__in=self.get_queryset())
        qs = qs.annotate(
            order_count=Count('product__order'),
            average_price=Avg('product__order__price')
        )
        df = pd.DataFrame([
                {
                    "name": i.name,
                    "order_count": i.average_price
                } for i in qs
            ]
        )
        context['category_names'] = list(df.name)
        context['category_values'] = list(df.order_count)

        # Server-side generation
        try:
            cr = datetime.datetime.fromtimestamp(
                os.path.getmtime(path)
            )
            file_age = (datetime.datetime.now() - cr).seconds
        except:
            file_age = 100 * 60 * 24
        if file_age > 120:
            plot = sns.barplot(data=df, x="name", y="order_count")
            plot.get_figure().savefig(path)

        # ES
        s = ES_CLIENT.search(index="orders", query={"match_all": {}})
        context['es_result'] = s['hits']['hits']
        return context

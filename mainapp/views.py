from django.views.generic import ListView

from mainapp.models import *


class OrderListView(ListView):
    template_name = "order_list.html"
    model = Order
    queryset = Order.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['len_clients'] = Client.objects.count()
        return context


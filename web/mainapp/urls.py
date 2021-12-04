from django.urls import path, include
from .views import *

app_name = 'mainapp'

urlpatterns = [
    path("", OrderListView.as_view()),
    path("get_order_plot_data/", get_order_plot_data),
]

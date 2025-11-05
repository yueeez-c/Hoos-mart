from django.urls import path
from . import views

urlpatterns = [
    path("", views.buy_marketplace, name="marketplace-buy"),      # /marketplace/
    path("sell/", views.sell_marketplace, name="marketplace-sell"),  # /marketplace/sell/
]

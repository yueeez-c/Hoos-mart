from django.urls import path
from . import views

urlpatterns = [
    path("", views.buy_marketplace, name="marketplace-buy"),      # /marketplace/
    path("sell/", views.sell_marketplace, name="marketplace-sell"),  # /marketplace/sell/
    path("<int:pk>/", views.listing_detail, name="listing-detail"),
    path("listing/<int:pk>/edit/", views.edit_listing, name="marketplace-edit"),
    path("listing/<int:pk>/delete/", views.delete_listing, name="marketplace-delete"),
    path("<int:pk>/", views.listing_detail, name="marketplace-detail"),
    path("", views.listing_list, name="marketplace-list"),
    path("<int:pk>/", views.listing_detail, name="marketplace-detail"),
]

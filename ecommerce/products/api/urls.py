from django.urls import path
from products.api.views import (
    ProductListView,
    ProductDetailView,
    CartView,
    ClearCartView,
    RemoveSpecificItemView,
    DecreaseItemQuantityView,
    AddToCartView,
    ShippingAddressView
    )


app_name = 'products'


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-cart/', CartView.as_view(), name='my-cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('clear-cart/', ClearCartView.as_view(), name='clear-cart'),
    path('remove-specific-item/', RemoveSpecificItemView.as_view(), name='remove-specific-item'),
    path('decrease-item-quantity/', DecreaseItemQuantityView.as_view(), name='decrease-item-quantity'),
    path('shipping-address/', ShippingAddressView.as_view(), name='shipping-address'),
]


from django.urls import path
from products.api.views import (
    ProductListView,
    ProductDetailView,
    CartView,
    ClearCart,
    RemoveSpecificItem,
    DecreaseItemQuantity,
    AddToCart
    )


app_name = 'products'


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-cart/', CartView.as_view(), name='my-cart'),
    path('add-to-cart/', AddToCart.as_view(), name='add-to-cart'),
    path('clear-cart/', ClearCart.as_view(), name='clear-cart'),
    path('remove-specific-item/', RemoveSpecificItem.as_view(), name='remove-specific-item'),
    path('decrease-item-quantity/', DecreaseItemQuantity.as_view(), name='decrease-item-quantity'),
]


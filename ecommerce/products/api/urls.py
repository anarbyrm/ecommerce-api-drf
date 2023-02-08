from django.urls import path
from products.api.views import ProductListView, ProductDetailView

app_name = 'products'


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    
]

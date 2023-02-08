from rest_framework import generics, status, permissions
from products.api.serializers import ProductListSerializer, ProductDetailSerializer
from products.models import Product


class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    
    
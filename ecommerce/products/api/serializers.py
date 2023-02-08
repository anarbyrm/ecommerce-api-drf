from rest_framework.serializers import ModelSerializer
from products.models import Product


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'slug', 'image')
        
        
class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'image', 'price', 'slug')
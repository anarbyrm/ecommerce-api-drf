from rest_framework import serializers
from products.models import Product, Cart, CartItem


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'slug',
            'image'
            )
        
        
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'image',
            'price',
            'slug'
            )


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = (
            'cart',
            'product',
            'quantity',
            'total_price'
        )

    def get_total_price(self, obj: CartItem):
        return obj.get_total_price()

        
class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    
        
    class Meta:
        model = Cart
        fields = (
            'uuid',
            'user',
            'completed',
            'cart_items',
            'total_price',
            'item_count'
        )
        
    def get_cart_items(self, obj: Cart):
        items = obj.items.all()
        if items.exists():
            return CartItemSerializer(items, many=True).data
        return []
    
    def get_total_price(self, obj: Cart):
        return obj.get_total_price()
    
    def get_item_count(self, obj: Cart):
        return obj.get_item_count()
    
    
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from products.api.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CartSerializer,
    CartItemSerializer
    )
from products.models import (
    Product,
    Cart,
    CartItem
    )


class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    
    
class CartView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        serializer = CartSerializer(cart)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AddToCart(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart = Cart.objects.get_or_create(user=self.request.user, completed=False)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        serializer = CartItemSerializer(item)
        serializer.data['message'] = 'Item added to the cart!'
        
        if not created:
            item.quantity += 1
            item.save()
            serializer.data['message'] = 'Item quantity increased!'
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ClearCart(generics.GenericAPIView):
    def delete(self, request):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        items = CartItem.object.filter(cart=cart)
        
        if items.exists():
            for item in items:
                item.delete()
            
        return Response({'message': 'All items inside the cart has been removed!'}, status=status.HTTP_204_NO_CONTENT)
    

class RemoveSpecificItem(generics.GenericAPIView):
    def delete(self, request):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        item =  CartItem.objects.filter(cart=cart)
        
        if item.exists():
            item = item.first()
            item_name = item.product.name
            item.delete()
            
        return Response({'message': f'{item_name} removed completely form the cart!'}, status=status.HTTP_204_NO_CONTENT)
    

class DecreaseItemQuantity(generics.GenericAPIView):
    def put(self, request):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        item =  CartItem.objects.filter(cart=cart)
        
        if item.exists():
            item = item.first()
            
            item.quantity -= 1
            item.save()
            
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
            
    
    
    
    
    
    
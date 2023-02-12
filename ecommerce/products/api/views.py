from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, mixins, views
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from products.api.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CartSerializer,
    CartItemSerializer,
    AddressSerializer
    )
from products.models import (
    Product,
    Cart,
    CartItem,
    ShippingAddress
    )


class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    
    
class CartView(views.APIView):
    def get(self, request, *arg, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)    
        print(cart, Cart.objects.count())    
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class AddToCartView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, slug, *arg, **kwargs):
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
    
    
class ClearCartView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *arg, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        items = CartItem.object.filter(cart=cart)
        
        if items.exists():
            for item in items:
                item.delete()
            
        return Response({'message': 'All items inside the cart has been removed!'}, status=status.HTTP_204_NO_CONTENT)
    

class RemoveSpecificItemView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *arg, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        item =  CartItem.objects.filter(cart=cart)
        
        if item.exists():
            item = item.first()
            item_name = item.product.name
            item.delete()
            
        return Response({'message': f'{item_name} removed completely form the cart!'}, status=status.HTTP_204_NO_CONTENT)
    

class DecreaseItemQuantityView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, slug, *arg, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user, completed=False)
        product = get_object_or_404(Product, slug=slug)
        item =  CartItem.objects.filter(cart=cart, product=product)
        
        if item.exists():
            item = item.first()
            item.quantity -= 1
            item.save()
            
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
            
class ShippingAddressView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
        
    def get_object(self):
        address = ShippingAddress.objects.filter(user=self.request.user)
        if address.exists():
            obj = address.first()
            return obj
        return None
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response({'message': 'shipping address for the user is not defined.'})
        serializer = AddressSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        if self.get_object() is None:
            serializer = AddressSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            instance = self.get_object()
            serializer = AddressSerializer(instance, data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
    
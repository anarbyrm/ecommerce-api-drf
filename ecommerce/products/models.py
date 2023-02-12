from uuid import uuid4
from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ImageField(upload_to='product/')
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(null=True, blank=True, unique=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-updated_at', '-created_at')
        

class Cart(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    completed = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'cart: {self.user}'
    
    def get_item_count(self) -> int:
        return sum(item.quantity for item in self.items.all())
    
    def get_total_price(self) -> float:
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'product')
        ordering = ('-updated_at',)
    
    def __str__(self):
        return f'{self.cart}: {self.product} x {self.quantity}'
    
    def get_total_price(self) -> float:
        return self.quantity * self.product.price
    

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    full_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user}: {self.full_address}"
    
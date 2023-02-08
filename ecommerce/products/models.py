from uuid import uuid4
from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Product(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ImageField(upload_to='product/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.cart}: {self.product} x {self.quantity}'
    
    def get_total_price(self) -> float:
        return self.quantity * self.product.price
    
    


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    completed = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} cart'
    
    def get_item_count(self) -> int:
        return sum(item.quantity for item in self.items.all())
    
    def get_total_price(self) -> float:
        return sum(item.get_total_price() for item in self.items.all())
    
    
    


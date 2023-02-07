from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra):
        if email is None:
            raise TypeError('Users should have a Email')
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra):
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user    
    

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=225, unique=True)
    password = models.CharField(max_length=225)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    
    def __str__(self):
        return self.email
    
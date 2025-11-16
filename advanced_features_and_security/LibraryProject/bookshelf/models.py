from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class Book(models.Model):
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=100)
    publication_year= models.IntegerField()
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
class User(AbstractUser):
    username= models.CharField(max_length=100, unique=True)
    password= models.CharField(max_length=100)
    email= models.EmailField(unique=True)
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    date_of_birth= models.DateField()
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

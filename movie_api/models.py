import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, Permission
#from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField(('year'), validators=[MinValueValidator(1878), max_value_current_year])
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/images/', null=True, blank=True)
    age_rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}"
    
class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('regular', 'Regular User'),
        ('admin', 'Administrator'),
    )
    email = models.EmailField(unique=True)
    birthday = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='regular')

    def __str__(self):
        return self.username
    

class RegularUserPermission(Permission):
    def has_permission(self, request, view):
        return request.user.role == 'regular'

class AdminUserPermission(Permission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'
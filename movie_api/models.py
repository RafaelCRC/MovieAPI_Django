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
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

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

class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        super(MovieRating, self).save(*args, **kwargs)
        self.update_movie_average_rating()

    def update_movie_average_rating(self):
        ratings = self.movie.ratings.all()
        total_ratings = ratings.count()
        average_rating = sum(rating.rating for rating in ratings) / total_ratings if total_ratings > 0 else 0
        self.movie.average_rating = round(average_rating, 2)
        self.movie.save()

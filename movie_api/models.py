import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

    def __str__(self):
        return f"{self.title}"
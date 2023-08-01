from django.contrib import admin
from .models import Movie, User

admin.site.register([Movie, User])
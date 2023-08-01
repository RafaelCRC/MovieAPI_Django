"""
URL configuration for movie_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

from .views import movie_list, movie_detail_id, UserRegistrationView, UserLoginView, UserListCreateView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', movie_list, name='movie-list'),
    path('movies/<int:id>', movie_detail_id, name='movie-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),

    
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
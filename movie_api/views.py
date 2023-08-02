from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
#from django.http import JsonResponse
from .models import Movie, User, RegularUserPermission, AdminUserPermission, MovieRating
from .serializers import MovieSerializer, UserSerializer, UserCRUDSerializer, MovieRatingSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import date

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_list(request):

    paginator = CustomPageNumberPagination()

    if request.method == 'GET':
        title = request.GET.get('title', None)
        user_age = None
        if request.user.birthday:
            user_age = (date.today() - request.user.birthday).days // 365

        if title:
            movies = Movie.objects.filter(title__icontains=title)
        else:
            movies = Movie.objects.all()

        if user_age:
            movies = movies.filter(age_rating__lte=user_age)

        paginated_movies = paginator.paginate_queryset(movies, request)
        serializer = MovieSerializer(paginated_movies, many=True)
        #return JsonResponse({ 'movies': serializer.data }, safe=False, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_detail_id(request, id):

    try:
        movie = Movie.objects.get(pk=id)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)
    
    user_age = None
    if request.user.birthday:
        user_age = (date.today() - request.user.birthday).days // 365

    if request.method == 'GET':
        if user_age and movie.age_rating > user_age:
            return Response({"error": "You are not allowed to view this movie."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if user_age and movie.age_rating > user_age:
            return Response({"error": "You are not allowed to update this movie."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if user_age and movie.age_rating > user_age:
            return Response({"error": "You are not allowed to update this movie."}, status=status.HTTP_403_FORBIDDEN)
        
        movie.delete()
        return Response({"message": "Movie deleted."}, status=status.HTTP_204_NO_CONTENT)

class UserRegistrationView(CreateAPIView):  # regular registration (can only create regular users)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListCreateView(generics.ListCreateAPIView):  # only for admin users
    queryset = User.objects.all()
    serializer_class = UserCRUDSerializer
    permission_classes = [IsAuthenticated, AdminUserPermission]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): # only for admin users
    queryset = User.objects.all()
    serializer_class = UserCRUDSerializer
    permission_classes = [IsAuthenticated, AdminUserPermission]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted."}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class UserLoginView(TokenObtainPairView):
    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_movie_rating(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user  # Get the authenticated user from the request

    # Check if the user has already rated this movie
    if MovieRating.objects.filter(movie=movie, user=user).exists():
        return Response({"error": "You have already rated this movie."}, status=status.HTTP_400_BAD_REQUEST)

    # Add the movie and user to the request data to create the rating
    request.data["movie"] = movie_id
    request.data["user"] = user.id

    serializer = MovieRatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
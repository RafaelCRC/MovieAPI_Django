from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#from django.http import JsonResponse
from .models import Movie, User, RegularUserPermission, AdminUserPermission
from .serializers import MovieSerializer, UserSerializer, UserCRUDSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
def movie_list(request):

    paginator = CustomPageNumberPagination()

    if request.method == 'GET':
        title = request.GET.get('title', None)

        if title:
            movies = Movie.objects.filter(title__icontains=title)
        else:
            movies = Movie.objects.all()

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
def movie_detail_id(request, id):

    try:
        movie = Movie.objects.get(pk=id)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
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
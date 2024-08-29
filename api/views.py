from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from .models import Movie, Actor
from .serializer import MovieSerializer, ActorSerializer, ActorNameSerializer
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.db.models import Count
from rest_framework.exceptions import ValidationError
# Create your views here.


#To search movies and update movie details from the result
class MovieDetailView(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all().prefetch_related('genres', 'actors', 'technicians', 'director')
    serializer_class = MovieSerializer
    lookup_field = 'name' 
    # queryset = Movie.objects.all()
    # serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        movie_name = kwargs.get('name')
        movie = get_object_or_404(Movie, name=movie_name)
        serializer = self.get_serializer(movie)
        return Response(serializer.data)

#To list movies associated with an actor, director or technician
class MovieFilter(filters.FilterSet):
    director = filters.CharFilter(field_name="director", lookup_expr='icontains')
    actors = filters.CharFilter(field_name="actors__name", lookup_expr='icontains')
    technicians = filters.CharFilter(field_name="technicians__name", lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['director', 'actors', 'technicians']

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter


#To list actors and movies associated with them
class ActorNameListView(generics.ListAPIView):
    queryset = Actor.objects.annotate(movie_count=Count('movies'))
    serializer_class = ActorNameSerializer


#To delete actors who is not associated with any movies
class ActorDeleteView(generics.DestroyAPIView):
    serializer_class = ActorSerializer

    def get_object(self):
        actor_name = self.kwargs.get('name')
        actor = get_object_or_404(Actor, name=actor_name)
        return actor

    def delete(self, request, *args, **kwargs):
        actor = self.get_object()
        # Check if actor is associated with any movies
        if actor.movies.count() > 0:
            raise ValidationError("Cannot delete actor associated with movies.")
        return super().delete(request, *args, **kwargs)

# class ActorDeleteView(generics.DestroyAPIView):
#     queryset = Actor.objects.annotate(movie_count=Count('movies')).filter(movie_count=0)
#     serializer_class = ActorSerializer

#     def delete(self, request, *args, **kwargs):
#         actor_name = kwargs.get('name')
#         actor = get_object_or_404(Actor, name=actor_name)
#         if actor.movies.count() > 0:
#             raise ValidationError("Cannot delete actor associated with movies.")
#         return super().delete(request, *args, **kwargs)
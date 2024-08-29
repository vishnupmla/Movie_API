from django.urls import path,include
from .views import MovieDetailView, MovieListView, ActorDeleteView, ActorNameListView

urlpatterns = [
     path('movies/<str:name>/', MovieDetailView.as_view(), name='movie-detail'),
     path('movies/', MovieListView.as_view(), name='movie-list'),
     path('actors/<str:name>/delete/', ActorDeleteView.as_view(), name='actor-delete'),
     path('actors/', ActorNameListView.as_view(), name='actor-name-list'),
]

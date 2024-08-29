from rest_framework import serializers
from .models import Genre, Actor, Technician, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class ActorNameSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ['name', 'movie_count']

    def get_movie_count(self, obj):
        return obj.movies.count()

class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    actors = serializers.PrimaryKeyRelatedField(many=True, queryset=Actor.objects.all())
    technicians = serializers.PrimaryKeyRelatedField(many=True, queryset=Technician.objects.all())

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        actors = validated_data.pop('actors')
        technicians = validated_data.pop('technicians')
        movie = Movie.objects.create(**validated_data)
        movie.genres.set(genres)
        movie.actors.set(actors)
        movie.technicians.set(technicians)
        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres', None)
        actors = validated_data.pop('actors', None)
        technicians = validated_data.pop('technicians', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if genres is not None:
            instance.genres.set(genres)
        if actors is not None:
            instance.actors.set(actors)
        if technicians is not None:
            instance.technicians.set(technicians)

        instance.save()
        return instance

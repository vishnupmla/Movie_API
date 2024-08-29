from django.contrib import admin

# Register your models here.
from .models import Genre, Actor, Technician, Movie

admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Technician)
admin.site.register(Movie)
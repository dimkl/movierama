from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
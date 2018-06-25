from rest_framework.serializers import ModelSerializer, ALL_FIELDS

from .models import Movie


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ALL_FIELDS

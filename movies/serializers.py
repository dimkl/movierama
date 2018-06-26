from rest_framework import serializers

from .models import Movie
from users.serializers import UserSerializer

class MovieSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
        
    class Meta:
        model = Movie
        exclude = ('updated_at', )

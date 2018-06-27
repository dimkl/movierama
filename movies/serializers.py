from rest_framework import serializers

from .models import Movie, MovieOpinion
from users.serializers import UserSerializer

class MovieSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
        
    class Meta:
        model = Movie
        exclude = ('updated_at', )


class MovieOpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieOpinion
        fields = ['opinion', ]
    
    def save(self, **kwargs):
        opinion, exists = MovieOpinion.objects.update_or_create(defaults=self.validated_data, **kwargs)
        
        # update movie likes|hates counter
        movie = opinion.movie
        movie.likes_counter = movie.likes.count()
        movie.hates_counter = movie.hates.count()
        
        movie.save(update_fields=['likes_counter', 'hates_counter'])
        
        return opinion
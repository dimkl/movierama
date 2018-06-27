from rest_framework import serializers

from movies.models import Movie, MovieOpinion
from users.serializers import UserSerializer


def user_of_request(serializer_instance):
    user = None
    request = serializer_instance.context.get("request")
    if request and hasattr(request, "user"):
        user = request.user
    
    return user


class MovieSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    is_liked = serializers.SerializerMethodField()
    is_hated = serializers.SerializerMethodField()
    is_opinion_disabled = serializers.SerializerMethodField()
    
    publication_date_since = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        exclude = ('updated_at', )

    def get_is_liked(self, instance):
        user = user_of_request(self)
        return user and user.is_authenticated() and instance.likes.filter(user=user).exists()
    
    def get_is_hated(self, instance):
        user = user_of_request(self)
        return user and user.is_authenticated() and instance.hates.filter(user=user).exists()
    
    def get_is_opinion_disabled(self, instance):
        user = user_of_request(self)
        return not user or not user.is_authenticated() or instance.user == user
    
    def get_publication_date_since(self, instance):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(instance.publication_date)

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
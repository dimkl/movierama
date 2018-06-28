from django.test import TestCase

from movies.serializers import MovieSerializer
from movies.models import OPINION_LIKE, OPINION_HATE
from movies.factory import (
    get_sample_users,
    get_sample_movies,
    set_sample_opinion,
    get_sample_request
)

class MovieSerializerTests(TestCase):
    def test_liked_movie_is_marked(self):
        """
        Ensure that movie is_liked attribute is marked for liked movie.
        """
        users = get_sample_users()
        movie = get_sample_movies(users)[0]
        user = users[-1]
        set_sample_opinion(user, movie, OPINION_LIKE)
        
        request = get_sample_request(user)
        data = MovieSerializer(instance=movie, context={'request': request}).data
        self.assertTrue(data['is_liked'])

    def test_not_liked_movie_is_not_marked(self):
        """
        Ensure that movie is_liked attribute is not marked for movie that is 
        not liked by that user.
        """
        users = get_sample_users()
        movie = get_sample_movies(users)[0]
        user = users[-1]
        other_user =  users[-2]
        
        set_sample_opinion(user, movie, OPINION_LIKE)
        
        request = get_sample_request(other_user)
        data = MovieSerializer(instance=movie, context={'request': request}).data
        self.assertFalse(data['is_liked'])
    
    def test_hated_movie_is_marked(self):
        """
        Ensure that movie is_hated attribute is marked for hated movie.
        """
        users = get_sample_users()
        movie = get_sample_movies(users)[0]
        user = users[-1]
        set_sample_opinion(user, movie, OPINION_HATE)
        
        request = get_sample_request(user)
        data = MovieSerializer(instance=movie, context={'request': request}).data
        self.assertTrue(data['is_hated'])

    def test_not_hated_movie_is_not_marked(self):
        """
        Ensure that movie is_hated attribute is not marked for movie that is 
        not hated by that user.
        """
        users = get_sample_users()
        movie = get_sample_movies(users)[0]
        user = users[-1]
        other_user =  users[-2]
        
        set_sample_opinion(user, movie, OPINION_HATE)
        
        request = get_sample_request(other_user)
        data = MovieSerializer(instance=movie, context={'request': request}).data
        self.assertFalse(data['is_hated'])
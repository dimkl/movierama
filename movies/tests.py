from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Movie
from movies.serializers import MovieSerializer
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta

class MovieViewSetCreateTests(APITestCase):
    def test_create_movie_authenticated_user(self):
        """
        Ensure that authenticated user can create a new movie object.
        """
        User = get_user_model()
        user = User.objects.create(username='aloha', first_name='F', last_name='L')
        publication_date = now() 
                
        url = reverse('movie-list')
        data = {'title': 'Movie title', 'description': 'Description' }
        
        # authenticate user
        self.client.force_authenticate(user=user)
        # submit request
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # assert request result
        self.assertEqual(Movie.objects.count(), 1)
        movie = Movie.objects.get()
        # check response data
        self.assertEqual(response.data, MovieSerializer(instance=movie).data)
        # check inserted data
        self.assertEqual(movie.title, 'Movie title')
        self.assertEqual(movie.description, 'Description')
        self.assertEqual(movie.user, user)
        self.assertAlmostEqual(movie.publication_date, publication_date, 
                                delta=timedelta(seconds=1))

    def test_create_movie_anonymous_user(self):
        """
        Ensure that anonymous user cannot create a new movie object .
        """
        url = reverse('movie-list')
        data = {'title': 'Movie title', 'description': 'Description' }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movie.objects.count(), 0)

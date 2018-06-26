from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Movie, MovieOpinion, OPINION_LIKE, OPINION_HATE
from movies.serializers import MovieSerializer
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from unittest import skip
from django.db.models import Count
from django.conf import settings


def get_paginated_queryset(qs):
    page = settings.REST_FRAMEWORK['PAGE_SIZE']
    return qs[0:page]

def get_sample_users():
    # create some users
    users = [get_user_model().objects.create(username='mitsos{}'.format(i)) for i in xrange(0,4)]
    return users


def get_sample_movies(users):
    user = users[0]
    # create some movies
    movies = [Movie.objects.create(title=str(m), description=str(m), user=user, air_date=now()) for m in range(0,4)]
    Movie.objects.create(title='5', description='5', user=user, air_date=now())
    
    return movies


def set_sample_opinions(users, movies, opinion):
     # add likes
    for index, user in enumerate(users):
        for movie_index in range(index,4):
            MovieOpinion.objects.create(user=user, 
                                        movie=movies[movie_index], 
                                        opinion=opinion)
    # update aggregation fields
    for movie in movies:
        movie.likes_counter = movie.likes.count()
        movie.hates_counter = movie.hates.count()
        movie.save()


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

class MovieViewSetOrderingTests(APITestCase):

    def test_ordering_descending_likes(self):
        """
        Ensure that anonymous user can order movies by descending likes.
        """
        url = '{}?ordering=-{}'.format(reverse('movie-list'), 'likes_counter')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        set_sample_opinions(users, movies, OPINION_LIKE)
       
        # apply request   
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # create expected response data
        qs = get_paginated_queryset(Movie.objects.order_by('-likes_counter'))
        expected_response = MovieSerializer(qs, many=True).data

        self.assertEqual(response.data['results'], expected_response)
    
    def test_ordering_asceding_likes(self):
        """
        Ensure that anonymous user can order movies by asceding likes.
        """
        url = '{}?ordering={}'.format(reverse('movie-list'), 'likes_counter')
        
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        set_sample_opinions(users, movies, OPINION_LIKE)

        # apply request   
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # create expected response data
        qs = get_paginated_queryset(Movie.objects.order_by('likes_counter'))
        expected_response = MovieSerializer(qs, many=True).data

        self.assertEqual(response.data['results'], expected_response)
        
    def test_ordering_descending_hates(self):
        """
        Ensure that anonymous user can order movies by descending hates.
        """
        url = '{}?ordering=-{}'.format(reverse('movie-list'), 'hates_counter')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        set_sample_opinions(users, movies, OPINION_HATE)

        # apply request   
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # create expected response data
        qs = get_paginated_queryset(Movie.objects.order_by('-hates_counter'))
        expected_response = MovieSerializer(qs, many=True).data

        self.assertEqual(response.data['results'], expected_response)
    
    def test_ordering_asceding_hates(self):
        """
        Ensure that anonymous user can order movies by asceding hates.
        """
        url = '{}?ordering={}'.format(reverse('movie-list'), 'hates_counter')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        set_sample_opinions(users, movies, OPINION_HATE)
    
        # apply request   
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # create expected response data
        qs = get_paginated_queryset(Movie.objects.order_by('hates_counter'))
        expected_response = MovieSerializer(qs, many=True).data
    
        self.assertEqual(response.data['results'], expected_response)

    def test_ordering_descending_publication_date(self):
        """
        Ensure that anonymous user can order movies by descending publication_date.
        """
        url = '{}?ordering=-{}'.format(reverse('movie-list'), 'publication_date')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        qs = get_paginated_queryset(Movie.objects.order_by('-publication_date'))
        expected_response = MovieSerializer(qs, many=True).data
        
        self.assertEqual(response.data['results'], expected_response)
    
    def test_ordering_asceding_publication_date(self):
        """
        Ensure that anonymous user can order movies by asceding publication_date.
        """
        url = '{}?ordering={}'.format(reverse('movie-list'), 'publication_date')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        qs = get_paginated_queryset(Movie.objects.order_by('publication_date'))
        expected_response = MovieSerializer(qs, many=True).data
        
        self.assertEqual(response.data['results'], expected_response)
    
    def test_ordering_descending_air_date(self):
        """
        Ensure that anonymous user can order movies by descending air_date.
        """
        url = '{}?ordering=-{}'.format(reverse('movie-list'), 'air_date')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        qs = get_paginated_queryset(Movie.objects.order_by('-air_date'))
        expected_response = MovieSerializer(qs, many=True).data
        self.assertEqual(response.data['results'], expected_response)
    
    def test_ordering_asceding_air_date(self):
        """
        Ensure that anonymous user can order movies by asceding air_date.
        """
        url = '{}?ordering={}'.format(reverse('movie-list'), 'air_date')
        # setup sample data   
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        qs = get_paginated_queryset(Movie.objects.order_by('air_date'))
        expected_response = MovieSerializer(qs, many=True).data
        self.assertEqual(response.data['results'], expected_response)

class MovieListViewSetTests(APITestCase):
    def test_list_movies(self):
        """
        Ensure that anonymous user can get all movies.
        """
        url = reverse('movie-list')
         
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        qs = get_paginated_queryset(Movie.objects.all())
        expected_response = MovieSerializer(qs, many=True).data
        self.assertEqual(response.data['results'], expected_response)

class MovieListByUserViewSetTests(APITestCase):
    def test_list_movies_by_user(self):
        """
        Ensure that anonymous user can get movies filtered by user submitted them.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        search_username = users[0].username
        url = '{}?search={}'.format(reverse('movie-list'), search_username)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        qs = get_paginated_queryset(Movie.objects.filter(user__username=search_username))
        self.assertNotEqual(qs.count, 0)

        expected_response = MovieSerializer(qs, many=True).data
        self.assertEqual(response.data['results'], expected_response)
    
    def test_list_movies_by_undefined_user(self):
        """
        Ensure that anonymous user can get no movies filtered by user submitted 
        them for an username that does not exist.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        search_username = users[0].username+'undefined'
        url = '{}?search={}'.format(reverse('movie-list'), search_username)
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        qs = get_paginated_queryset(Movie.objects.filter(user__username=search_username))
        self.assertEqual(qs.count(), 0)
        
        expected_response = MovieSerializer(qs, many=True).data
        self.assertEqual(response.data['results'], expected_response)

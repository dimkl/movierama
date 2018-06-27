from datetime import timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.conf import settings

from .models import Movie, MovieOpinion, OPINION_LIKE, OPINION_HATE
from .serializers import MovieSerializer


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
    [set_sample_opinion(user, movies[movie_index], opinion)
    for index, user in enumerate(users) 
    for movie_index in range(index,4)]


def set_sample_opinion(user, movie, opinion):
    # set already liked movie by user
    opinion = MovieOpinion.objects.create(
                            user=user, 
                            movie=movie, 
                            opinion=opinion)
   
    # update movie likes|hates counter
    movie = opinion.movie
    movie.likes_counter = movie.likes.count()
    movie.hates_counter = movie.hates.count()
    
    movie.save(update_fields=['likes_counter', 'hates_counter'])


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
        self.assertNotEqual(qs.count(), 0)

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


class MovieOpinionViewSetTests(APITestCase):
    
    def test_like_movie_not_owner(self):
        """
        Ensure that not owner of a movie can like a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_LIKE }
        
        self.client.force_authenticate(user=not_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(MovieOpinion.objects.count(), 1)
        
        movie.refresh_from_db()
        expected_response = MovieSerializer(movie).data
        self.assertEqual(response.data, expected_response)
        
        self.assertEqual(movie.likes_counter, 1)
        self.assertEqual(movie.likes.count(), 1)

    def test_like_movie_owner(self):
        """
        Ensure that owner of a movie cannot like a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_LIKE }
        
        self.client.force_authenticate(user=movie.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(MovieOpinion.objects.count(), 0)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.likes_counter, 0)
        self.assertEqual(movie.likes.count(), 0)
    
    def test_cannot_like_already_liked_movie(self):
        """
        Ensure that user cannot like a movie already liked by him.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_LIKE)
        
        self.assertEqual(movie.likes_counter, 1)
        self.assertEqual(movie.likes.count(), 1)
        
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_LIKE }
        self.client.force_authenticate(user=not_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(MovieOpinion.objects.count(), 1)
        
        movie.refresh_from_db()
        expected_response = MovieSerializer(movie).data
        self.assertEqual(response.data, expected_response)
        
        self.assertEqual(movie.likes_counter, 1)
        self.assertEqual(movie.likes.count(), 1)
    
    def test_hate_movie_not_owner(self):
        """
        Ensure that not owner of a movie can hate a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_HATE }
        
        self.client.force_authenticate(user=not_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(MovieOpinion.objects.count(), 1)
        
        movie.refresh_from_db()
        expected_response = MovieSerializer(movie).data
        self.assertEqual(response.data, expected_response)
        
        self.assertEqual(movie.hates_counter, 1)
        self.assertEqual(movie.hates.count(), 1)

    def test_hate_movie_owner(self):
        """
        Ensure that owner of a movie cannot hate a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_HATE }
        
        self.client.force_authenticate(user=movie.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(MovieOpinion.objects.count(), 0)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.hates_counter, 0)
        self.assertEqual(movie.hates.count(), 0)
    
    def test_cannot_hate_already_hated_movie(self):
        """
        Ensure that user cannot hate a movie already hated by him.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_HATE)

        self.assertEqual(movie.hates.count(), 1)
        self.assertEqual(movie.hates_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_HATE }
        self.client.force_authenticate(user=not_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(MovieOpinion.objects.count(), 1)
        
        movie.refresh_from_db()
        expected_response = MovieSerializer(movie).data
        self.assertEqual(response.data, expected_response)
        
        self.assertEqual(movie.hates_counter, 1)
        self.assertEqual(movie.hates.count(), 1)

    def test_undo_like_movie_not_owner(self):
        """
        Ensure that not owner of a movie can undo the like of a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_LIKE)

        self.assertEqual(movie.likes.count(), 1)
        self.assertEqual(movie.likes_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': None }
        self.client.force_authenticate(user=not_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        expected_response = MovieSerializer(movie).data
        self.assertEqual(response.data, expected_response)
        
        self.assertEqual(movie.likes_counter, 0)
        self.assertEqual(movie.likes.count(), 0)

    def test_undo_like_movie_owner(self):
        """
        Ensure that owner of a movie cannot undo the like of a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_LIKE)

        self.assertEqual(movie.likes.count(), 1)
        self.assertEqual(movie.likes_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': None }
        
        self.client.force_authenticate(user=users[0])
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.likes_counter, 1)
        self.assertEqual(movie.likes.count(), 1)
    
    def test_cannot_undo_like_of_other_user(self):
        """
        Ensure that owner of a movie cannot undo the like of other user for a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        other_user = users[-2]
        
        set_sample_opinion(other_user, movie, OPINION_LIKE)

        self.assertEqual(movie.likes.count(), 1)
        self.assertEqual(movie.likes_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': None }
        
        self.client.force_authenticate(user=not_owner)
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.likes_counter, 1)
        self.assertEqual(movie.likes.count(), 1)
    
    def test_undo_hate_movie_not_owner(self):
        """
        Ensure that not owner of a movie can undo the hate of a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_HATE)

        self.assertEqual(movie.hates.count(), 1)
        self.assertEqual(movie.hates_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': None }
        self.client.force_authenticate(user=not_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        expected_response = MovieSerializer(movie).data
        self.assertEqual(response.data, expected_response)
        
        self.assertEqual(movie.hates_counter, 0)
        self.assertEqual(movie.hates.count(), 0)

    def test_undo_hate_movie_owner(self):
        """
        Ensure that owner of a movie cannot undo the hate of a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_HATE)

        self.assertEqual(movie.hates.count(), 1)
        self.assertEqual(movie.hates_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': None }
        
        self.client.force_authenticate(user=users[0])
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.hates_counter, 1)
        self.assertEqual(movie.hates.count(), 1)
    
    def test_cannot_undo_hate_of_other_user(self):
        """
        Ensure that owner of a movie cannot undo the hate of other user for a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        other_user = users[-2]
        
        set_sample_opinion(other_user, movie, OPINION_HATE)

        self.assertEqual(movie.hates.count(), 1)
        self.assertEqual(movie.hates_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': None }
        
        self.client.force_authenticate(user=not_owner)
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.hates_counter, 1)
        self.assertEqual(movie.hates.count(), 1)
        
    def test_cannot_hate_and_like_movie(self):
        """
        Ensure that user cannot hate and like at the same time a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data_like = {'opinion': OPINION_LIKE }
        data_hate = {'opinion': OPINION_HATE }
        
        self.client.force_authenticate(user=not_owner)
        
        response_like = self.client.post(url, data_like, format='json')
        self.assertEqual(response_like.status_code, status.HTTP_200_OK)
        
        response_hate = self.client.post(url, data_hate, format='json')
        self.assertEqual(response_hate.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
                
        self.assertEqual(movie.hates_counter, 1)
        self.assertEqual(movie.hates.count(), 1)

        self.assertEqual(movie.likes.count(), 0)
        self.assertEqual(movie.likes_counter, 0)
    
    def test_cannot_like_hate_and_movie(self):
        """
        Ensure that user cannot like and hate at the same time a movie.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data_like = {'opinion': OPINION_LIKE }
        data_hate = {'opinion': OPINION_HATE }
        
        self.client.force_authenticate(user=not_owner)
        
        response_hate = self.client.post(url, data_hate, format='json')
        self.assertEqual(response_hate.status_code, status.HTTP_200_OK)
        
        response_like = self.client.post(url, data_like, format='json')
        self.assertEqual(response_like.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.likes.count(), 1)
        self.assertEqual(movie.likes_counter, 1)
        
        self.assertEqual(movie.hates_counter, 0)
        self.assertEqual(movie.hates.count(), 0)

    def test_hate_already_liked_movie(self):
        """
        Ensure that user removes like of a movie when opinion changes to hate.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_LIKE)

        self.assertEqual(movie.likes.count(), 1)
        self.assertEqual(movie.likes_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_HATE }
        
        self.client.force_authenticate(user=not_owner)
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.hates_counter, 1)
        self.assertEqual(movie.hates.count(), 1)
        
        self.assertEqual(movie.likes.count(), 0)
        self.assertEqual(movie.likes_counter, 0)
        
    def test_like_already_hated_movie(self):
        """
        Ensure that user removes hate of a movie when opinion changes to like.
        """
        users = get_sample_users()
        movies = get_sample_movies(users)
        
        movie = movies[0]
        not_owner = users[-1]
        
        set_sample_opinion(not_owner, movie, OPINION_HATE)

        self.assertEqual(movie.hates.count(), 1)
        self.assertEqual(movie.hates_counter, 1)
                
        url = reverse('movie-opinion', kwargs={'pk': movies[0].pk})
        data = {'opinion': OPINION_LIKE }
        
        self.client.force_authenticate(user=not_owner)
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        movie.refresh_from_db()
        
        self.assertEqual(movie.likes.count(), 1)
        self.assertEqual(movie.likes_counter, 1)
        
        self.assertEqual(movie.hates_counter, 0)
        self.assertEqual(movie.hates.count(), 0)
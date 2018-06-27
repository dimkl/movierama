from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
from django.conf import settings
from django.http import HttpRequest

from movies.models import Movie, MovieOpinion


def get_paginated_queryset(qs):
    """
    Get queryset limited using rest_framework page size.
    
    Args:
        qs(django.db.models.QuerySet): queryset to be paginated

    Returns:
        django.db.models.QuerySet: The limited queryset
    """
    page = settings.REST_FRAMEWORK['PAGE_SIZE']
    return qs[0:page]


def get_sample_users(number=4, username_format='mitsos{}'):
    """
    Create sample users.
    
    Args:
        number(int): number of sample users to be created.
        username_format (str): username format to be used in username generation

    Returns:
        list<django.conf.settings.AUTH_USER_MODEL>: list of users
    """
    return [get_user_model().objects.create(username=username_format.format(i)) for i in xrange(0,number)]



def get_sample_movies(users, number=4):
    """
    Create sample movies.
    
    Args:
        users(list<django.conf.settings.AUTH_USER_MODEL>): list of users
        number(int): number of sample movies to be created

    Returns:
        list<movies.models.Movie>: list of movies
    """
    owner = users[0]
    return [Movie.objects.create(title=str(m), description=str(m), user=owner, air_date=now().date()) for m in range(0, number)]


def set_sample_opinions(users, movies, opinion):
    """
    Create sample opinions for users and movies using a defined opinion.
    
    Args:
        users(list<django.conf.settings.AUTH_USER_MODEL>): list of users
        movies(list<movies.models.Movie>): list of movies
        opinion(str): movies.models.OPINION_LIKE | movies.models.OPINION_HATE | None
    """
    [set_sample_opinion(user, movies[movie_index], opinion)
    for index, user in enumerate(users) 
    for movie_index in range(index,4)]


def set_sample_opinion(user, movie, opinion):
    """
    Create sample opinion for user, movie and opinion.
    
    Args:
        user(django.conf.settings.AUTH_USER_MODEL): 
        movie(movies.models.Movie): 
        opinion(str): movies.models.OPINION_LIKE | movies.models.OPINION_HATE | None
    """
    # set liked movie by user
    opinion = MovieOpinion.objects.create(
                            user=user, 
                            movie=movie, 
                            opinion=opinion)
   
    # update movie likes|hates counter
    movie = opinion.movie
    movie.likes_counter = movie.likes.count()
    movie.hates_counter = movie.hates.count()
    
    movie.save(update_fields=['likes_counter', 'hates_counter'])


def get_sample_request(user=None):
    """
    Create sample django http request for authenticated or anonymous user.
    
    Args:
        user(django.conf.settings.AUTH_USER_MODEL): 
    
    Returns:
        django.http.HttpRequest: dummy http request with user
    """
    request = HttpRequest()
    request.user = user if user else AnonymousUser()
    
    return request

from django.conf.urls import url, include

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from movies import viewsets

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'movies', viewsets.MovieViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^docs/', include_docs_urls(title='Movierama API')),
    url(r'^', include(router.urls))
]
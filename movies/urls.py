from django.conf.urls import url
from movies.views import MoviesListView, MovieView

urlpatterns = [
    url(r'^$',MoviesListView.as_view(), name='list'),
    url(r'^(?P<pk>[\d]+)$',MovieView.as_view(), name='detail'),
]

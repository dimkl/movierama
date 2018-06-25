from django.views.generic import TemplateView


class MoviesListView(TemplateView):
    template_name = 'movies/list.html'

class MovieView(TemplateView):
    template_name = 'movies/detail.html'
    
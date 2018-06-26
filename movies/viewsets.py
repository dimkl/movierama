from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(mixins.ListModelMixin, 
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('likes', 'hates', 'publication_date', 'air_date')
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Purchase.objects.filter(purchaser__username=username)
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]

        return super(MovieViewSet, self).get_permissions()

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create Movie resource endpoint allowed only to authenticated users.
        
        request:
        
            {
                title(str): (required) max-length: 255 , 
                description(str): (required),
                air_date(datetime): (optional)
            }
        
        response:
            
           {
               id(int): movie id,
               user(dict):  { first_name(str):,last_name(str):,id(int):},
               title(str): max length 255,
               description(str):,
               air_date(datetime): datetime or null,
               publication_date(datetime):
           }
        
        http codes:

            200: on failure
            201: on success
            403: on user without permission
            
        """
        return super(MovieViewSet, self).create(request, *args, **kwargs)

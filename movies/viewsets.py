from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Movie, OPINION_LIKE, OPINION_HATE
from .serializers import MovieSerializer
from core.api import IsNotOwner


class MovieViewSet(mixins.ListModelMixin, 
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('likes_counter', 'hates_counter', 'publication_date', 'air_date', )
    search_fields = ('=user__username', )
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        
        if self.action in ['like', 'hate', 'reset_opinion']:
            self.permission_classes = [IsNotOwner]
        
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
    
    def list(self, request, *args, **kwargs):
        """
        Get all Movie resources endpoint allowed to any user paginated by 20.
        
        request:
        
            {}
        
        response:
            
           { 
            count:()
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
        return super(MovieViewSet, self).list(request, *args, **kwargs)
    
    @detail_route(methods=['put'])
    def opinion(self, request, *args, **kwargs):
        """
        
        """
        
    
    # @detail_route(methods=['post'])
    # def hate(self, request, *args, **kwargs):
    #     pass

    # @detail_route(methods=['post'])
    # def reset_opinion(self, request, *args, **kwargs):
    #     pass
    
from django.http import Http404

from rest_framework import mixins, viewsets, filters, status, exceptions
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import Movie, OPINION_LIKE, OPINION_HATE
from .serializers import MovieSerializer, MovieOpinionSerializer


class MovieViewSet(mixins.ListModelMixin, 
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('likes_counter', 'hates_counter', 'publication_date', 'air_date', )
    search_fields = ('=user__username', )
    
    def check_object_permissions(self, request, instance):
        if self.action == 'opinion':
            if  instance.user == request.user:
                raise exceptions.PermissionDenied
                
        return super(MovieViewSet, self).check_object_permissions(request, instance)
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        
        return super(MovieViewSet, self).get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_owner(self, instance):
        return 
        
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
                likes_counter(int):
                hates_counter(int):
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
                count(int):
                results(list): list of models
                previous(str): link to fetch previous resources
                next(str): link to fetch previous resources
               
           }
        
        model:
            
            {
                id(int): movie id,
                user(dict):  { first_name(str):,last_name(str):,id(int):},
                title(str): max length 255,
                description(str):,
                air_date(datetime): datetime or null,
                publication_date(datetime):
                likes_counter(int):
                hates_counter(int):
            }
    
        http codes:

            200: on failure
            201: on success
            403: on user without permission
            
        """
        return super(MovieViewSet, self).list(request, *args, **kwargs)
    
    @detail_route(methods=['post'])
    def opinion(self, request, *args, **kwargs):
        """
        Set your opinion about a Movie resource.
        
        request:
            {
                opinion(str): (required) L|H|null
            }
        
        response:
            
            {
                id(int): movie id,
                user(dict):  { first_name(str):,last_name(str):,id(int):},
                title(str): max length 255,
                description(str):,
                air_date(datetime): datetime or null,
                publication_date(datetime):
                likes_counter(int):
                hates_counter(int):
            }
        
        model:
            
            {
                id(int): movie id,
                user(dict):  { first_name(str):,last_name(str):,id(int):},
                title(str): max length 255,
                description(str):,
                air_date(datetime): datetime or null,
                publication_date(datetime):
            }
    
        http codes:

            200: on failure|success
            403: on user without permission
            400: on invalid movie id
        """
        response_data = {}
        status_code = status.HTTP_200_OK
        serializer = MovieOpinionSerializer(data=request.data)
        
        try:
            instance = self.get_object()
            serializer.is_valid(True)
            
            opinion = serializer.save(user=request.user, movie=instance)
            response_data = MovieSerializer(instance=opinion.movie).data
        except Http404 as e:
            response_data['error'] = 'Movie with pk `{}` does not exist'.format(kwargs.get('pk'))
            status_code = status.HTTP_400_BAD_REQUEST
        # except Exception as e:
        #     response_data['error'] = 'Exception `{}`'.format(unicode(e))

        return Response(response_data, status=status_code)
 
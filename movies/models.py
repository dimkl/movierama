from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    air_date =  models.DateTimeField(null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    
    likes_counter = models.PositiveSmallIntegerField(default=0)    
    hates_counter = models.PositiveSmallIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def likes(self):
        return self.opinions.filter(opinion=OPINION_LIKE)
    
    @property
    def hates(self):
        return self.opinions.filter(opinion=OPINION_HATE)


OPINION_LIKE = 'L'
OPINION_HATE = 'H'

class MovieOpinion(models.Model):
    OPINION_CHOICES = (
        (OPINION_LIKE, _('like')),
        (OPINION_HATE, _('hate')),
    ) 

    user =  models.ForeignKey(settings.AUTH_USER_MODEL, related_name='opinions')
    movie = models.ForeignKey('movies.Movie', related_name='opinions')
    opinion = models.CharField(max_length=1, choices=OPINION_CHOICES, 
                                null=True, blank=True)
    
    class Meta:
        unique_together = ( 
            ('user', 'movie'),
        )
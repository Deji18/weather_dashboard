from django.db import models
from django.conf import settings

class WeatherPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    temperature = models.FloatField()
    conditions = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    agrees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='weather_agrees')
    disagrees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='weather_disagrees')

# Create your models here.

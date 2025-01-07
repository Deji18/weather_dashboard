# serializers.py
from rest_framework import serializers
from .models import WeatherPost

class WeatherPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherPost
        fields = ['id', 'location', 'temperature', 'conditions', 'agrees', 'disagrees', 'created_at']
# weather/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WeatherPost

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class WeatherPostForm(forms.ModelForm):
    class Meta:
        model = WeatherPost
        fields = ['location']
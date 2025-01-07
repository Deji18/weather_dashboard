# from django.shortcuts import render
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import WeatherPost
# import requests
# from decouple import config

# def get_weather(city):
#     api_key = config('you_api_key')
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
#     response = requests.get(url)
#     return response.json()

# @login_required
# def dashboard(request):
#     if request.method == 'POST':
#         location = request.POST.get('location')
#         weather_data = get_weather(location)
        
#         if weather_data.get('main'):
#             WeatherPost.objects.create(
#                 user=request.user,
#                 location=location,
#                 temperature=weather_data['main']['temp'],
#                 conditions=weather_data['weather'][0]['description']
#             )
    
#     weather_posts = WeatherPost.objects.all().order_by('-created_at')
#     return render(request, 'weather/dashboard.html', {'posts': weather_posts})


# Create your views here.
import os
import queue
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import requests
from rest_framework import viewsets, permissions
from .serializers import WeatherPostSerializer
from .models import WeatherPost
from .forms import WeatherPostForm
from django.conf import settings



class WeatherPostViewSet(viewsets.ModelViewSet):
    queryset = WeatherPost.objects.all()
    serializer_class = WeatherPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def get_weather(city):
    """Get weather data from OpenWeatherMap API"""
    api_key = settings.OPENWEATHER_API_KEY
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException:
        return None

@login_required
def dashboard(request):
    """Main dashboard view"""
    if request.method == 'POST':
        location = request.POST.get('location')
        if location:
            weather_data = get_weather(location)
            
            if weather_data and weather_data.get('main'):
                WeatherPost.objects.create(
                    user=request.user,
                    location=location,
                    temperature=weather_data['main']['temp'],
                    conditions=weather_data['weather'][0]['description']
                )
                messages.success(request, 'Weather post created successfully!')
            else:
                messages.error(request, 'Could not fetch weather data for this location.')
        
    # Get all weather posts, newest first
    weather_posts = WeatherPost.objects.all().order_by('-created_at')
    return render(request, 'weather/dashboard.html', {
        'posts': weather_posts
    })

@login_required
def toggle_agreement(request, post_id, agree):
    """Handle agree/disagree functionality"""
    post = get_object_or_404(WeatherPost, id=post_id)
    
    if agree == 'agree':
        # Remove from disagrees if present
        if request.user in post.disagrees.all():
            post.disagrees.remove(request.user)
        # Toggle agrees
        if request.user in post.agrees.all():
            post.agrees.remove(request.user)
        else:
            post.agrees.add(request.user)
    else:
        # Remove from agrees if present
        if request.user in post.agrees.all():
            post.agrees.remove(request.user)
        # Toggle disagrees
        if request.user in post.disagrees.all():
            post.disagrees.remove(request.user)
        else:
            post.disagrees.add(request.user)
    
    return redirect('dashboard')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Adjust to your login URL name
    else:
        form = UserCreationForm()
    return render(request, 'weather/register.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(WeatherPost, id=post_id)
    if request.user != post.user:
        messages.error(request, 'You cannot edit this post!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = WeatherPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('dashboard')
    else:
        form = WeatherPostForm(instance=post)
    return render(request, 'weather/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(WeatherPost, id=post_id)
    if request.user != post.user:
        messages.error(request, 'You cannot delete this post!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')
    return render(request, 'weather/delete_confirm.html', {'post': post})

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = WeatherPost.objects.filter(
            queue(location__icontains=query) |
            queue(conditions__icontains=query) |
            queue(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        posts = WeatherPost.objects.all().order_by('-created_at')
    return render(request, 'weather/search_results.html', {'posts': posts, 'query': query})
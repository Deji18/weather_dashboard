from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('search/', views.search_posts, name='search_posts'),
    path('toggle-agreement/<int:post_id>/<str:agree>/', views.toggle_agreement, name='toggle_agreement'),
]
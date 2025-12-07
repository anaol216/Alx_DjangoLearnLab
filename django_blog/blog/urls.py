"""
URL configuration for the blog app.

Maps URLs to views for displaying blog content, user authentication,
and CRUD operations for blog posts.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
<<<<<<< HEAD
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    SearchResultView, PostByTagListView
=======
    CommentCreateView, CommentUpdateView, CommentDeleteView
>>>>>>> 482b9eaeb153fb3b0dc7e02dc4eab126209c23f5
)

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Blog Post CRUD URLs
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comment CRUD URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
<<<<<<< HEAD
    
    # Search and Tag URLs
    path('search/', views.SearchResultView.as_view(), name='search-results'),
    path('tags/<str:tag_slug>/', views.PostByTagListView.as_view(), name='post-by-tag'),
=======
>>>>>>> 482b9eaeb153fb3b0dc7e02dc4eab126209c23f5
]

"""
Views for the Blog application.

This module contains views for displaying blog posts and handling
user interactions with the blog.
"""

from django.shortcuts import render
from .models import Post


def home(request):
    """
    Home page view - displays all blog posts.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered home.html template with list of posts
    """
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

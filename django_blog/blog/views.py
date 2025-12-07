"""
Views for the Blog application.

This module contains views for displaying blog posts, user authentication,
and profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm


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


def register(request):
    """
    User registration view.
    
    Handles GET requests by displaying the registration form.
    Handles POST requests by validating and creating new user.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered registration form or redirect to login on success
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """
    User profile view and update.
    
    Displays user profile information and handles profile updates.
    Requires user to be logged in.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered profile page with update form
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})

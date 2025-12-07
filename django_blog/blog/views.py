"""
Views for the Blog application.

This module contains views for displaying blog posts, user authentication,
profile management, and CRUD operations for blog posts.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm


# ============================================================================
# Home and Authentication Views
# ============================================================================

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


# ============================================================================
# Blog Post CRUD Views (Class-Based)
# ============================================================================

class PostListView(ListView):
    """
    Display a list of all blog posts.
    
    Accessible to all users (authenticated and unauthenticated).
    Posts are ordered by published_date in descending order (newest first).
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(DetailView):
    """
    Display a single blog post with full content.
    
    Accessible to all users (authenticated and unauthenticated).
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post.
    
    Only accessible to authenticated users.
    The author is automatically set to the logged-in user.
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the author to the current user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing blog post.
    
    Only accessible to the post's author.
    Uses UserPassesTestMixin to verify ownership.
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Ensure the author remains the original author."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the post author."""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post.
    
    Only accessible to the post's author.
    Uses UserPassesTestMixin to verify ownership.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        """Check if the current user is the post author."""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)

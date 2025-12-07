"""
Views for the Blog application.

This module contains views for displaying blog posts, user authentication,
profile management, and CRUD operations for blog posts and comments.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm


# ============================================================================
# Home and Authentication Views
# ============================================================================

def home(request):
    """Home page view - displays all blog posts."""
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def register(request):
    """User registration view."""
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
    """User profile view and update."""
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
# Blog Post CRUD Views
# ============================================================================

class PostListView(ListView):
    """Display a list of all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(DetailView):
    """Display a single blog post with full content."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Add comment form and comments to context."""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post."""
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing blog post."""
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Comment CRUD Views
# ============================================================================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new comment on a post.
    Handles the submission from the post detail page or a separate form.
    """
    model = Comment
    form_class = CommentForm
    # We don't need a template_name if we redirect back to detail view on error,
    # but generic views usually expect one.
    # However, we'll mostly use this via the detail view or a dedicated simple form page if needed.
    template_name = 'blog/comment_form.html' 
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been posted!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        messages.success(self.request, 'Comment update successfully')
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def get_success_url(self):
        # We need to get the post PK before deletion, which happens in delete()
        # But get_success_url is called after objects deletion usually or before.
        # Safe way is to store post pk in delete method or use self.object.post.pk if available.
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Search and Tag Views
# ============================================================================

from django.db.models import Q
from .models import Tag

class SearchResultView(ListView):
    """
    Search results view.
    Filters posts by title, content, or tags based on search query.
    """
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PostByTagListView(ListView):
    """
    Display posts filtered by a specific tag.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, name=tag_slug)
        return Post.objects.filter(tags=self.tag).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

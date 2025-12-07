"""
Blog Post Model

This module defines the Post model for the Django blog application.
The Post model represents individual blog posts with title, content,
publication date, and author information.
"""

from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    """
    Represents a blog post.
    
    Attributes:
        title (CharField): The title of the blog post, max 200 characters.
        content (TextField): The main content/body of the blog post.
        published_date (DateTimeField): Auto-set timestamp when post is created.
        author (ForeignKey): Reference to the User who authored the post.
    
    The author field uses CASCADE deletion, meaning if a user is deleted,
    all their posts will also be deleted.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-published_date']  # Newest posts first
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment on a blog Post.
    
    Attributes:
        post: Reference to the Post the comment belongs to.
        author: Reference to the User who wrote the comment.
        content: The text content of the comment.
        created_at: Timestamp when comment was created.
        updated_at: Timestamp when comment was last updated.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

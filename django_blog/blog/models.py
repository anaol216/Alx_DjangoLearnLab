"""
Blog Post Model

This module defines the Post model for the Django blog application.
The Post model represents individual blog posts with title, content,
publication date, and author information.
"""

from django.db import models
from django.contrib.auth.models import User


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
    
    class Meta:
        ordering = ['-published_date']  # Newest posts first
    
    def __str__(self):
        return self.title

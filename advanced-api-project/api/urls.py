"""
URL configuration for the API app.

This module defines URL patterns for all Book API endpoints, mapping URLs to
their corresponding views.
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books
    # GET /api/books/
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID
    # GET /api/books/<int:pk>/
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book
    # POST /api/books/create/
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book
    # PUT/PATCH /api/books/<int:pk>/update/
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book
    # DELETE /api/books/<int:pk>/delete/
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]

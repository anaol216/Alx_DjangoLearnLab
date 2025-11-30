"""
Views for the API app.

This module contains Django REST Framework generic views for handling CRUD operations
on the Book model. Each view is designed to handle specific operations with proper
permissions and customizations.
"""

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view provides read-only access to all books in the database.
    Supports filtering, searching, and ordering capabilities.
    
    Permissions:
        - IsAuthenticatedOrReadOnly: Anyone can view, but only authenticated users
          can perform write operations (though this view is read-only).
    
    Features:
        - Filtering: Filter books by author or publication_year
        - Searching: Search books by title
        - Ordering: Sort books by any field
    
    Endpoint: GET /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by ID.
    
    This view provides read-only access to a specific book instance.
    
    Permissions:
        - IsAuthenticatedOrReadOnly: Anyone can view book details.
    
    Endpoint: GET /api/books/<int:pk>/
    
    Parameters:
        pk (int): Primary key of the book to retrieve
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    This view allows authenticated users to create new book instances.
    The BookSerializer handles validation, including ensuring the publication_year
    is not in the future.
    
    Permissions:
        - IsAuthenticated: Only authenticated users can create books.
    
    Validation:
        - All fields are validated by BookSerializer
        - Custom validation ensures publication_year is not in the future
        - Author must exist in the database
    
    Endpoint: POST /api/books/create/
    
    Request Body:
        {
            "title": "Book Title",
            "publication_year": 2023,
            "author": 1
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom create method to handle additional logic if needed.
        
        Currently uses default behavior but can be extended to:
        - Set additional fields
        - Send notifications
        - Log creation events
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    This view allows authenticated users to update book instances.
    Supports both full updates (PUT) and partial updates (PATCH).
    
    Permissions:
        - IsAuthenticated: Only authenticated users can update books.
    
    Validation:
        - All fields are validated by BookSerializer
        - Custom validation ensures publication_year is not in the future
    
    Endpoint: PUT/PATCH /api/books/update/<int:pk>/
    
    Parameters:
        pk (int): Primary key of the book to update
    
    Request Body (PUT - all fields required):
        {
            "title": "Updated Title",
            "publication_year": 2023,
            "author": 1
        }
    
    Request Body (PATCH - partial update):
        {
            "title": "Updated Title"
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        """
        Custom update method to handle additional logic if needed.
        
        Currently uses default behavior but can be extended to:
        - Track modification history
        - Send update notifications
        - Log update events
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    This view allows authenticated users to delete book instances.
    
    Permissions:
        - IsAuthenticated: Only authenticated users can delete books.
    
    Endpoint: DELETE /api/books/delete/<int:pk>/
    
    Parameters:
        pk (int): Primary key of the book to delete
    
    Response:
        - 204 No Content on successful deletion
        - 404 Not Found if book doesn't exist
        - 403 Forbidden if user is not authenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        """
        Custom delete method to handle additional logic if needed.
        
        Currently uses default behavior but can be extended to:
        - Soft delete instead of hard delete
        - Archive deleted records
        - Send deletion notifications
        - Log deletion events
        """
        instance.delete()

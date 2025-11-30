"""
Serializers for the API app.

This module contains serializers for the Author and Book models, handling
the conversion between complex Django model instances and Python datatypes
that can be easily rendered into JSON, XML, or other content types.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Serializes all fields of the Book model including the foreign key relationship
    to the Author model. Includes custom validation to ensure the publication_year
    is not in the future.
    
    Fields:
        - id: Auto-generated primary key
        - title: Book title
        - publication_year: Year the book was published
        - author: Foreign key reference to the Author model
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated publication_year value
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    Serializes the Author model with a nested representation of related books.
    The 'books' field uses the BookSerializer to dynamically serialize all books
    associated with the author through the one-to-many relationship.
    
    Relationship Handling:
        - The 'books' field is a nested serializer that represents the reverse
          relationship from Author to Book (defined by related_name='books' in the
          Book model's ForeignKey).
        - Setting many=True allows serialization of multiple Book instances.
        - Setting read_only=True prevents books from being created/updated through
          the AuthorSerializer (books should be managed through BookSerializer).
    
    Fields:
        - id: Auto-generated primary key
        - name: Author's name
        - books: Nested list of all books written by this author
    """
    
    # Nested serializer for related books
    # 'many=True' because one author can have multiple books
    # 'read_only=True' because we don't want to create/update books through the author endpoint
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

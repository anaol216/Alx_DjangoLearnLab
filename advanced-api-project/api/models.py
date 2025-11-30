"""
Models for the API app.

This module defines the data models for a book management system, including
Author and Book models with a one-to-many relationship.
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores information about authors who have written books.
    An author can have multiple books associated with them through a
    one-to-many relationship.
    
    Fields:
        name (CharField): The author's full name. Maximum length of 200 characters.
    
    Relationships:
        books: Reverse relationship to Book model. Access all books by this author
               using author.books.all() due to the related_name='books' in the
               Book model's ForeignKey.
    
    Methods:
        __str__: Returns the author's name for string representation.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String representation of the Author model.
        
        Returns:
            str: The author's name.
        """
        return self.name


class Book(models.Model):
    """
    Book model representing a book with title, publication year, and author.
    
    This model stores information about books and establishes a one-to-many
    relationship with the Author model. Each book must be associated with
    exactly one author, while an author can have multiple books.
    
    Fields:
        title (CharField): The book's title. Maximum length of 200 characters.
        publication_year (IntegerField): The year the book was published.
                                         Should be validated to not be in the future.
        author (ForeignKey): Reference to the Author model establishing the
                            one-to-many relationship.
    
    Relationships:
        author: Many-to-one relationship with Author model.
                - on_delete=CASCADE: If an author is deleted, all their books are deleted.
                - related_name='books': Allows reverse lookup from Author to Books
                  using author.books.all().
    
    Methods:
        __str__: Returns the book's title for string representation.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    # ForeignKey establishes a many-to-one relationship: many books can have one author
    # on_delete=CASCADE ensures that when an author is deleted, all their books are also deleted
    # related_name='books' allows accessing an author's books via author.books.all()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        """
        String representation of the Book model.
        
        Returns:
            str: The book's title.
        """
        return self.title

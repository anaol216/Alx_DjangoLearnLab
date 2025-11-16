"""
Django forms for the bookshelf app.

These forms provide secure input validation and sanitization to prevent
SQL injection, XSS attacks, and other security vulnerabilities.
Using Django forms ensures all user input is properly validated and escaped.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    
    This form provides:
    - Automatic HTML escaping to prevent XSS attacks
    - Input validation to prevent invalid data
    - Type conversion and sanitization
    - CSRF protection when used in templates
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200',  # Enforce model's max_length
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100',  # Enforce model's max_length
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': '1000',  # Reasonable minimum year
                'max': '9999',  # Reasonable maximum year
            }),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
            'publication_year': 'Publication Year',
        }
        help_texts = {
            'title': 'Enter the full title of the book (max 200 characters)',
            'author': 'Enter the author\'s name (max 100 characters)',
            'publication_year': 'Enter the year the book was published (4 digits)',
        }
    
    def clean_title(self):
        """
        Validate and sanitize the title field.
        
        This method:
        - Strips whitespace
        - Validates length
        - Prevents potentially dangerous input patterns
        """
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError('Title is required.')
        
        # Strip leading/trailing whitespace
        title = title.strip()
        
        # Check minimum length
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        
        # Check for potentially dangerous patterns (basic check)
        # Django's template system will handle HTML escaping, but we can add extra validation
        dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onload=']
        title_lower = title.lower()
        for pattern in dangerous_patterns:
            if pattern in title_lower:
                raise ValidationError('Title contains invalid characters.')
        
        return title
    
    def clean_author(self):
        """
        Validate and sanitize the author field.
        """
        author = self.cleaned_data.get('author')
        
        if not author:
            raise ValidationError('Author is required.')
        
        # Strip whitespace
        author = author.strip()
        
        # Check minimum length
        if len(author) < 2:
            raise ValidationError('Author name must be at least 2 characters long.')
        
        return author
    
    def clean_publication_year(self):
        """
        Validate the publication year.
        
        This method:
        - Ensures the year is a valid integer
        - Checks for reasonable year range
        - Prevents SQL injection by using Django ORM (which parameterizes queries)
        """
        year = self.cleaned_data.get('publication_year')
        
        if year is None:
            raise ValidationError('Publication year is required.')
        
        # Validate year range (reasonable bounds)
        if year < 1000:
            raise ValidationError('Publication year must be 1000 or later.')
        
        if year > 9999:
            raise ValidationError('Publication year must be 9999 or earlier.')
        
        return year


class BookSearchForm(forms.Form):
    """
    Form for searching books.
    
    This form demonstrates secure search functionality that:
    - Uses Django ORM (parameterized queries) to prevent SQL injection
    - Validates and sanitizes search input
    - Escapes output in templates
    """
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or author...',
            'maxlength': '200',
        }),
        label='Search',
        help_text='Enter keywords to search for books by title or author',
    )
    
    def clean_query(self):
        """
        Clean and validate search query.
        
        This prevents:
        - SQL injection (by using Django ORM, not raw SQL)
        - XSS attacks (by escaping in templates)
        - Excessive input length
        """
        query = self.cleaned_data.get('query', '')
        
        if query:
            # Strip whitespace
            query = query.strip()
            
            # Basic validation - check for dangerous patterns
            # Note: Django templates automatically escape output, but we add extra validation
            dangerous_patterns = ['<script', 'javascript:', 'onerror=']
            query_lower = query.lower()
            for pattern in dangerous_patterns:
                if pattern in query_lower:
                    raise ValidationError('Search query contains invalid characters.')
        
        return query


class ExampleForm(forms.Form):
    """
    Example form demonstrating security best practices.
    
    This form serves as a reference for implementing secure forms with:
    - Input validation
    - HTML escaping
    - CSRF protection
    - Type checking
    - Sanitization
    """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'maxlength': '100',
        }),
        label='Name',
        help_text='Enter your full name (max 100 characters)',
    )
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'maxlength': '254',
        }),
        label='Email',
        help_text='Enter a valid email address',
    )
    
    message = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message (optional)',
            'maxlength': '500',
            'rows': 4,
        }),
        label='Message',
        help_text='Optional message (max 500 characters)',
    )
    
    def clean_name(self):
        """
        Validate and sanitize the name field.
        
        Security features:
        - Strips whitespace
        - Validates length
        - Checks for dangerous patterns
        """
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError('Name is required.')
        
        # Strip whitespace
        name = name.strip()
        
        # Check minimum length
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
        # Check for potentially dangerous patterns
        dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onload=']
        name_lower = name.lower()
        for pattern in dangerous_patterns:
            if pattern in name_lower:
                raise ValidationError('Name contains invalid characters.')
        
        return name
    
    def clean_message(self):
        """
        Validate and sanitize the message field.
        """
        message = self.cleaned_data.get('message', '')
        
        if message:
            # Strip whitespace
            message = message.strip()
            
            # Check for dangerous patterns
            dangerous_patterns = ['<script', 'javascript:', 'onerror=']
            message_lower = message.lower()
            for pattern in dangerous_patterns:
                if pattern in message_lower:
                    raise ValidationError('Message contains invalid characters.')
        
        return message


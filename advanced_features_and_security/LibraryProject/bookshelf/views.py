"""
Views for the bookshelf app with permission-based access control.

This module implements CRUD operations for Book model with proper permission checks:
- can_view: Required to view book lists and details
- can_create: Required to create new books
- can_edit: Required to edit existing books
- can_delete: Required to delete books

Security Features:
- All forms use Django forms for input validation (prevents SQL injection)
- CSRF protection via @csrf_protect decorator and {% csrf_token %} in templates
- Permission-based access control
- Input sanitization and validation
- Safe use of Django ORM (parameterized queries)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from .models import Book
from .forms import BookForm, BookSearchForm
from .forms import ExampleForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books with optional search functionality.
    
    Security Features:
    - Uses Django ORM for database queries (prevents SQL injection)
    - Search form validates and sanitizes input
    - All output is automatically escaped in templates
    
    Permission Required: bookshelf.can_view
    """
    books = Book.objects.all().order_by('title')
    search_form = BookSearchForm(request.GET or None)
    
    # Secure search using Django ORM (parameterized queries)
    # This prevents SQL injection attacks
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '').strip()
        if query:
            # Use Q objects for safe, parameterized queries
            # Django ORM automatically escapes and parameterizes these queries
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            ).order_by('title')
    
    context = {
        'books': books,
        'search_form': search_form,
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    Display details of a specific book.
    
    Permission Required: bookshelf.can_view
    """
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/book_detail.html', context)


@login_required
@csrf_protect
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book using Django forms for secure input validation.
    
    Security Features:
    - Uses Django ModelForm for automatic validation and sanitization
    - CSRF protection via @csrf_protect and {% csrf_token %} in template
    - Prevents SQL injection by using Django ORM (Book.objects.create)
    - Input validation prevents XSS and invalid data
    
    Permission Required: bookshelf.can_create
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Django forms automatically sanitize and validate input
            # Book.objects.create uses parameterized queries (prevents SQL injection)
            book = form.save()
            # Use format() instead of f-string for user input to be extra safe
            messages.success(request, 'Book "{}" created successfully!'.format(book.title))
            return redirect('bookshelf:book_detail', pk=book.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'form_type': 'Create'
    }
    return render(request, 'bookshelf/book_form.html', context)


@login_required
@csrf_protect
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book using Django forms for secure input validation.
    
    Security Features:
    - Uses Django ModelForm for automatic validation and sanitization
    - CSRF protection via @csrf_protect and {% csrf_token %} in template
    - Prevents SQL injection by using Django ORM (book.save())
    - Input validation prevents XSS and invalid data
    
    Permission Required: bookshelf.can_edit
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Django forms automatically sanitize and validate input
            # book.save() uses parameterized queries (prevents SQL injection)
            book = form.save()
            messages.success(request, 'Book "{}" updated successfully!'.format(book.title))
            return redirect('bookshelf:book_detail', pk=book.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'form_type': 'Edit'
    }
    return render(request, 'bookshelf/book_form.html', context)


@login_required
@csrf_protect
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book with CSRF protection.
    
    Security Features:
    - CSRF protection ensures only legitimate requests can delete
    - Uses Django ORM (book.delete()) which prevents SQL injection
    - Requires POST method (not GET) to prevent accidental deletions
    
    Permission Required: bookshelf.can_delete
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Store title before deletion for message
        book_title = book.title
        # Django ORM delete uses parameterized queries (prevents SQL injection)
        book.delete()
        messages.success(request, 'Book "{}" deleted successfully!'.format(book_title))
        return redirect('bookshelf:book_list')
    
    context = {'book': book}
    return render(request, 'bookshelf/book_confirm_delete.html', context)


@login_required
def book_permissions_info(request):
    """
    Display information about the current user's permissions.
    This view is accessible to all logged-in users.
    """
    user_permissions = {
        'can_view': request.user.has_perm('bookshelf.can_view'),
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    
    # Get user's groups
    user_groups = request.user.groups.all()
    
    context = {
        'user': request.user,
        'permissions': user_permissions,
        'groups': user_groups,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'bookshelf/permissions_info.html', context)

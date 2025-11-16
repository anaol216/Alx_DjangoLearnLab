"""
Views for the bookshelf app with permission-based access control.

This module implements CRUD operations for Book model with proper permission checks:
- can_view: Required to view book lists and details
- can_create: Required to create new books
- can_edit: Required to edit existing books
- can_delete: Required to delete books
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books.
    
    Permission Required: bookshelf.can_view
    """
    books = Book.objects.all().order_by('title')
    context = {
        'books': books,
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
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    
    Permission Required: bookshelf.can_create
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author and publication_year:
            try:
                book = Book.objects.create(
                    title=title,
                    author=author,
                    publication_year=int(publication_year)
                )
                messages.success(request, f'Book "{book.title}" created successfully!')
                return redirect('bookshelf:book_detail', pk=book.pk)
            except ValueError:
                messages.error(request, 'Invalid publication year. Please enter a valid number.')
        else:
            messages.error(request, 'All fields are required.')
    
    return render(request, 'bookshelf/book_form.html', {'form_type': 'Create'})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    
    Permission Required: bookshelf.can_edit
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author and publication_year:
            try:
                book.title = title
                book.author = author
                book.publication_year = int(publication_year)
                book.save()
                messages.success(request, f'Book "{book.title}" updated successfully!')
                return redirect('bookshelf:book_detail', pk=book.pk)
            except ValueError:
                messages.error(request, 'Invalid publication year. Please enter a valid number.')
        else:
            messages.error(request, 'All fields are required.')
    
    context = {
        'book': book,
        'form_type': 'Edit'
    }
    return render(request, 'bookshelf/book_form.html', context)


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book.
    
    Permission Required: bookshelf.can_delete
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
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

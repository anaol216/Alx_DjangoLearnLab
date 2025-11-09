from django.shortcuts import render
from django.http import HttpResponse
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)
# class Library(ListView):
#     model = Library
#     template_name = 'relationship_app/library_list.html'
#     context_object_name = 'libraries'
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
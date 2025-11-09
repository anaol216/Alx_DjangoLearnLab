from .views import LibraryDetailView, list_books, Library
from django.urls import path   

app_name = 'relationship_app'
urlpatterns = [
    path('books/',list_books, name='list_books'),
    path('libraries/', Library.as_view(), name='library_list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
from .views import list_books, Library, LibraryDetail
from django.urls import path   

app_name = 'relationship_app'
urlpatterns = [
    path('books/',list_books, name='list_books'),
    path('libraries/', Library.as_view(), name='library_list'),
    path('libraries/<int:pk>/', LibraryDetail.as_view(), name='library_detail'),
]
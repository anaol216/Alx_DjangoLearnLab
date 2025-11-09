from views import book_list, Library, LibraryDetail
from django.urls import path   

app_name = 'relationship_app'
urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('libraries/', Library.as_view(), name='library_list'),
    path('libraries/<int:pk>/', LibraryDetail.as_view(), name='library_detail'),
]
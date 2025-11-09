from .views import LibraryDetailView
from .views import list_books
from .views import Library
from django.urls import path
from authentication_app.views import register, user_login, user_logout    

app_name = 'relationship_app'
urlpatterns = [
    path('books/',list_books, name='list_books'),
    path('libraries/', Library.as_view(), name='library_list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
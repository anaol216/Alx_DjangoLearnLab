from .views import LibraryDetailView
from .views import list_books
from .views import Library
from django.urls import path, include
from . import views   
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'relationship_app'
urlpatterns = [
    path('books/',list_books, name='list_books'),
    path('libraries/', Library.as_view(), name='library_list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logged_out.html'), name='logout'),
]
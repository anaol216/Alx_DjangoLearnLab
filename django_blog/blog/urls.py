"""
URL configuration for the blog app.

Maps URLs to views for displaying blog content.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]

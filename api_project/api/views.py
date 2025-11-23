from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Book 

from .serializers import BookSerializer
from rest_framework import generics

class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

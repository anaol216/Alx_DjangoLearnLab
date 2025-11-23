from django.shortcuts import render

from rest_framework import viewsets
from .models import Book 

from .serializers import BookSerializer
from rest_framework import generics, viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class BookList(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer



class BookViewSet(viewsets.ModelViewSet):

     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated, IsAdminUser]

     queryset = Book.objects.all()  
     serializer_class = BookSerializer   

from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
urlpatterns = [
    path('books/', BookList.as_view(), name = 'book-list'),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

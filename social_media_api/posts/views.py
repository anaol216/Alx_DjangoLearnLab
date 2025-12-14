from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

class FeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')

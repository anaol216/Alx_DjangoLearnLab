from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Create notification for the post author
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked",
                    target=post
                )
            return Response({"message": "Post liked"})
        return Response({"message": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({"message": "Post unliked"})
        return Response({"message": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

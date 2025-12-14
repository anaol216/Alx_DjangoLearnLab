from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from accounts.models import CustomUser

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  # <- this line is required
        user = request.user

        # Check if the user already liked the post
        if Like.objects.filter(post=post, user=user).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the like
        Like.objects.create(post=post, user=user)
        
        # Optionally, create a notification here

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  # <- this line is required
        user = request.user

        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)

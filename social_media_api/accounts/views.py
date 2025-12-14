from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        return Response({"error": "You cannot follow yourself"}, status=400)

    request.user.following.add(user_to_follow)
    return Response({"message": f"You are now following {user_to_follow.username}"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

    request.user.following.remove(user_to_unfollow)
    return Response({"message": f"You unfollowed {user_to_unfollow.username}"})

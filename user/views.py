from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer, UserListSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username", "email")


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FollowUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        user_to_follow = generics.get_object_or_404(User, pk=pk)
        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.following.add(user_to_follow)
        return Response(
            {"detail": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        user_to_unfollow = generics.get_object_or_404(User, pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": f"You unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK,
        )


class UserFollowersListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()


class UserFollowingListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()

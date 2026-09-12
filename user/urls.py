from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import (
    CreateUserView,
    ManageUserView,
    UserListView,
    UserDetailView,
    FollowUserView,
    UserFollowersListView,
    UserFollowingListView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="profile"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/follow/", FollowUserView.as_view(), name="user-follow"),
    path("me/followers/", UserFollowersListView.as_view(), name="user-followers"),
    path("me/following/", UserFollowingListView.as_view(), name="user-following"),
]

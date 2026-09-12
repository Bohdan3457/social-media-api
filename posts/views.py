from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from posts.models import Like, Post
from posts.permission import IsAuthorOrReadOnly
from posts.serializers import (
    CommentSerializer,
    LikeSerializer,
    PostDetailSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title", "content")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="feed",
    )
    def feed(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="like")
    def like_toggle(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            return Response(
                {"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT
            )

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="comment")
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from posts.models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "text", "created_at")
        read_only_fields = ("id", "post", "author", "created_at")


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Like
        fields = ("id", "post", "user", "created_at")
        read_only_fields = ("id", "post", "user", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")
    likes_count = serializers.IntegerField(
        source="likes.count", read_only=True
    )
    comments_count = serializers.IntegerField(
        source="comments.count", read_only=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "image",
            "likes_count",
            "comments_count"
        )
        read_only_fields = ("id", "author", "created_at", "updated_at")

class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ("comments",)

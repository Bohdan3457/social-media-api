from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    followers_count = serializers.IntegerField(
        source="followers.count", read_only=True
    )
    following_count = serializers.IntegerField(
        source="following.count", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
            "followers_count",
            "following_count",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "required": False,
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_picture")

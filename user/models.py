import os
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return os.path.join("uploads", "users", f"{uuid.uuid4()}{ext}")


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to=user_image_file_path, null=True, blank=True
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    def __str__(self):
        return self.username

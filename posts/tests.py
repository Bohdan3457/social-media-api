from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post

User = get_user_model()


class PostApiTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="Password123!",
        )
        self.user2 = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="Password123!",
        )

        self.post = Post.objects.create(
            author=self.user1,
            title="Test Post Title",
            content="Test post content",
        )

        self.list_create_url = reverse("posts:post-list")
        self.detail_url = reverse(
            "posts:post-detail", kwargs={"pk": self.post.pk}
        )

    def test_list_posts_anonymous_success(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_authenticated_success(self):
        self.client.force_authenticate(user=self.user1)
        payload = {"title": "New Title", "content": "New Content"}
        response = self.client.post(self.list_create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post_by_author_success(self):
        self.client.force_authenticate(user=self.user1)
        payload = {"title": "Updated Title", "content": "Updated Content"}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_update_post_by_other_user_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        payload = {"title": "Hacked Title"}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_by_author_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

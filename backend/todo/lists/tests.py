from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo.lists.models import List
from todo.tasks.models import Task

__all__ = ["ListAPITests"]


User = get_user_model()


class ListAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="pass123",
        )

        response = self.client.post(
            reverse("auth:login"),
            {
                "username": "user",
                "password": "pass123",
            },
        )

        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_create_list(self):
        response = self.client.post(reverse("lists-list"), {"name": "My List"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(List.objects.first().user, self.user)

    def test_list_only_user_lists(self):
        List.objects.create(name="User List", user=self.user)
        List.objects.create(name="Other List", user=self.other_user)

        response = self.client.get(reverse("lists-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "User List")

    def test_retrieve_list_with_tasks(self):
        lst = List.objects.create(name="Test List", user=self.user)
        Task.objects.create(list=lst, title="Task 1")
        Task.objects.create(list=lst, title="Task 2")

        url = reverse("lists-detail", args=[lst.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["tasks"]), 2)

    def test_cannot_access_other_users_list(self):
        lst = List.objects.create(name="Other List", user=self.other_user)

        url = reverse("lists-detail", args=[lst.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

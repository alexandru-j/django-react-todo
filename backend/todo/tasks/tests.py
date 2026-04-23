from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo.lists.models import List
from todo.tasks.models import Task

__all__ = ["TaskAPITests"]


User = get_user_model()


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="pass123",
        )

        self.list = List.objects.create(name="User List", user=self.user)
        self.other_list = List.objects.create(name="Other List", user=self.other_user)

        response = self.client.post(
            reverse("auth:login"),
            {
                "username": "user",
                "password": "pass123",
            },
        )

        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_create_task(self):
        response = self.client.post(
            reverse("tasks-list"),
            {
                "list": self.list.id,
                "title": "New Task",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_cannot_create_task_in_other_users_list(self):
        response = self.client.post(
            reverse("tasks-list"),
            {
                "list": self.other_list.id,
                "title": "Hack Task",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_list_only_user_tasks(self):
        Task.objects.create(list=self.list, title="User Task")
        Task.objects.create(list=self.other_list, title="Other Task")

        response = self.client.get(reverse("tasks-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        task = Task.objects.create(list=self.list, title="Old Title")

        url = reverse("tasks-detail", args=[task.id])
        response = self.client.patch(url, {"title": "New Title"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "New Title")

    def test_delete_task(self):
        task = Task.objects.create(list=self.list, title="Task")

        url = reverse("tasks-detail", args=[task.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_cannot_access_other_users_task(self):
        task = Task.objects.create(list=self.other_list, title="Secret")

        url = reverse("tasks-detail", args=[task.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_complete_task(self):
        task = Task.objects.create(list=self.list, title="Task")

        url = reverse("tasks-complete", args=[task.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_cannot_complete_other_users_task(self):
        task = Task.objects.create(list=self.other_list, title="Other Task")

        url = reverse("tasks-complete", args=[task.id])
        response = self.client.post(url)

        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

        task.refresh_from_db()
        self.assertFalse(task.completed)

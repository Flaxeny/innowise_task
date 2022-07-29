from django.test import TestCase
from .celery import add

from rest_framework import status
from rest_framework.test import APITestCase
from chat.models import User
from chat.serializers import UserSerializer
from django.urls import reverse


class TestAddTask(TestCase):
  def setUp(self):
    self.task = add.apply_async(args=[3, 5])
    self.results = self.task.get()

  def test_task_state(self):
    self.assertEqual(self.task.state, "SUCCESS")

  def test_addition(self):
    self.assertEqual(self.results, 8)


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # (1)
        cls.users = [User.objects.create() for _ in range(3)]
        cls.user = cls.users[0]

    def test_can_browse_all_users(self):
        # (2)
        response = self.client.get(reverse("users:user-list"))

        # (3)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.users), len(response.data))

        for user in self.users:
            # (4)
            self.assertIn(
                UserSerializer(instance=self.user).data,
                response.data
            )

    def test_can_read_a_specific_user(self):
        # (5)
        response = self.client.get(
            reverse("users:user-detail", args=[self.user.id])
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            UserSerializer(instance=self.user).data,
            response.data
        )

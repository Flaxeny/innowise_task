from django.test import TestCase
from .celery import add


class TestAddTask(TestCase):
  def setUp(self):
    self.task = add.apply_async(args=[3, 5])
    self.results = self.task.get()

  def test_task_state(self):
    self.assertEqual(self.task.state, "SUCCESS")

  def test_addition(self):
    self.assertEqual(self.results, 8)


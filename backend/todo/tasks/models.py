from django.db import models

from todo.lists.models import List

__all__ = ["Task"]


class Task(models.Model):
    list = models.ForeignKey(List, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def complete(self):
        if not self.completed:
            self.completed = True
            self.save(update_fields=["completed"])

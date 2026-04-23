from django.contrib.auth import get_user_model
from django.db import models

__all__ = ["List"]

User = get_user_model()


class List(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="lists", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Task

__all__ = ["TaskSerializer", "TaskCreateSerializer"]


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "completed", "updated_at", "created_at"]
        read_only_fields = ["id", "updated_at", "created_at"]


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["list", "title"]

    def validate_list(self, value):
        if value.user != self.context["request"].user:
            raise ValidationError("You cannot add tasks to this list.")
        return value

from rest_framework.serializers import ModelSerializer

from todo.tasks.serializers import TaskSerializer

from .models import List

__all__ = ["ListSerializer", "ListDetailSerializer", "ListCreateSerializer"]


class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ["id", "name", "updated_at", "created_at"]


class ListDetailSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ["id", "name", "tasks", "updated_at", "created_at"]


class ListCreateSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ["name"]

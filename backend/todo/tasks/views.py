from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer

__all__ = ["TaskViewSet"]


class TaskViewSet(ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    serializer_create_class = TaskCreateSerializer

    def get_queryset(self):
        return self.model.objects.filter(list__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_create_class
        return self.serializer_class

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"])
    def complete(self, request, pk):
        task = self.get_object()
        task.complete()
        return Response(self.get_serializer(task).data)

from rest_framework.viewsets import ModelViewSet

from .models import List
from .serializers import ListCreateSerializer, ListDetailSerializer, ListSerializer

__all__ = ["ListViewSet"]


class ListViewSet(ModelViewSet):
    model = List
    serializer_class = ListSerializer
    serializer_create_class = ListCreateSerializer
    serializer_detail_class = ListDetailSerializer

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "create":
            return self.serializer_create_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

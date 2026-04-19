from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

__all__ = ["AccountSerializer"]

User = get_user_model()


class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

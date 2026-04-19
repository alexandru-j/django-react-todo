from rest_framework.generics import RetrieveAPIView

from .serializers import AccountSerializer

__all__ = ["AccountView"]


class AccountView(RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user

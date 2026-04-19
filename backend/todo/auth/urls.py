from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from .views import AccountView

app_name = "auth"

urlpatterns = [
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("@me/", AccountView.as_view(), name="account"),
]

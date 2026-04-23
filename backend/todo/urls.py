from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from todo.lists.views import ListViewSet
from todo.tasks.views import TaskViewSet

router = DefaultRouter()
router.register("lists", ListViewSet, basename="lists")
router.register("tasks", TaskViewSet, basename="tasks")

schema_view = get_schema_view(
    openapi.Info(
        title="Todo API",
        default_version="v1",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("todo.auth.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns), name="api"),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

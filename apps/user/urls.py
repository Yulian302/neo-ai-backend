from django.urls import re_path, path
from rest_framework.routers import DefaultRouter

from .notifications.views import *
from .settings.update.views import UpdateUserInfo
from .views import UserViewSet

user_router = DefaultRouter()
user_router.register(r"", UserViewSet, basename="")


urlpatterns = [
    re_path(r"update/", UpdateUserInfo.as_view()),
    path("notifications/<int:pk>/", UserNotificationDeleteView.as_view()),
    re_path(
        r"notifications/delete_all/$",
        UserNotificationDeleteAllView.as_view(),
    ),
] + user_router.urls

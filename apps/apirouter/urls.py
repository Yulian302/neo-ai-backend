from django.urls import include
from django.urls import path
from rest_framework import routers

from apps.security.csrf.views import CsrfToken
from apps.user.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("auth/", include("apps.auth.urls")),
    path("user/", include("apps.user.urls")),
    path("models/", include("apps.builtin_model.urls")),
    path("token/", include("apps.security.auth.simpleJwt.token_urls")),
    path("models/", include("apps.builtin_model.urls")),
    path("csrf/", CsrfToken.as_view()),
]

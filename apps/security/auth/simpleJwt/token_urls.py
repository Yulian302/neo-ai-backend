from django.urls import path, re_path
from .views import verify_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    re_path("^$", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path('verify/', verify_token),
]

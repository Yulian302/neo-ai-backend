from django.urls import re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    re_path("^$", TokenObtainPairView.as_view()),
    re_path("refresh/", TokenRefreshView.as_view()),
]

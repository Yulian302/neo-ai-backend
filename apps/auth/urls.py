from django.urls import re_path

from apps.auth.views import (
    RegisterView,
    SessionView,
    GoogleLoginApi,
    LoginView,
    LogoutView,
)

urlpatterns = [
    re_path(r"register/", RegisterView.as_view()),
    re_path(r"session/", SessionView.as_view()),
    re_path(r"login/google/$", GoogleLoginApi.as_view()),
    re_path(r"login/$", LoginView.as_view()),
    re_path(r"logout/", LogoutView.as_view()),
]

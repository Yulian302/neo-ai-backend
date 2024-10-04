from django.urls import re_path

from apps.auth.views import (
    RegisterView,
    LoginView,
    LogoutView,
)
from apps.auth.oauth2 import get_access_token, req_github_identity

urlpatterns = [
    re_path(r"register/", RegisterView.as_view()),
    re_path(r"login/$", LoginView.as_view()),
    re_path(r"logout/", LogoutView.as_view()),

    # github oauth2
    re_path(r"redirect-url/$", req_github_identity),
    re_path(r"callback/$", get_access_token)
]

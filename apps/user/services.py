# services.py
import os
from typing import Dict, Any
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
LOGIN_URL = f"{settings.BASE_APP_URL}/internal/login"


# Exchange authorization token with access token
def google_get_access_token(code: str, redirect_uri: str) -> str:
    data = {
        "code": code,
        "client_id": os.environ['GOOGLE_OAUTH2_CLIENT_ID'],
        "client_secret": os.environ['GOOGLE_OAUTH2_CLIENT_SECRET'],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    if not response.ok:
        raise ValidationError("Could not get access token from Google.")

    new_data = response.content
    access_token = data["access_token"]

    return access_token


# Get user info from google

def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    return response.json()


def get_user_data(validated_data):
    domain = settings.BASE_API_URL
    redirect_uri = f"{domain}/api/auth/login/google/"

    code = validated_data.get("code")
    error = validated_data.get("error")

    if error or not code:
        params = urlencode({"error": error})
        return redirect(f"{LOGIN_URL}?{params}")

    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)

    # Creates user in DB if first time login
    User.objects.get_or_create(
        username=user_data["email"],
        email=user_data["email"],
        first_name=user_data.get("given_name"),
        last_name=user_data.get("family_name"),
    )

    profile_data = {
        "email": user_data["email"],
        "first_name": user_data.get("given_name"),
        "last_name": user_data.get("family_name"),
    }
    return profile_data

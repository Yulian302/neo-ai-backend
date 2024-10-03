from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from requests import Response
import os
from django.contrib.auth.models import User


def req_github_identity(request):
    client_id = os.getenv("OAUTH2_GITHUB_CLIENT_ID")
    redirect_uri = os.getenv("OAUTH2_GITHUB_REDIRECT_URI")
    return HttpResponse(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}", 200)


def get_access_token(request):
    code = request.GET['code']
    # state = request.GET['state']
    client_secret = os.getenv("OAUTH2_GITHUB_CLIENT_SECRET")
    client_id = os.getenv("OAUTH2_GITHUB_CLIENT_ID")
    redirect_uri = os.getenv("OAUTH2_GITHUB_REDIRECT_URI")
    response = requests.post(
        "https://github.com/login/oauth/access_token", params={
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }, headers={
            "Accept": 'application/json'
        })
    if response.status_code == 200:
        return create_user(response)
    else:
        return JsonResponse({"message": "Could not receive access token!"}, 500)


def get_oauth2_user_data(access_token: str):
    user_data = requests.get("https://api.github.com/user", headers={
        "Authorization": f"Bearer {access_token}"
    }).json()
    return user_data


def create_user(user_data: Response):
    access_token = user_data.json()['access_token']
    user_info = get_oauth2_user_data(access_token)
    try:
        user = User.objects.get(username=user_info['login'])
    except User.DoesNotExist:
        user = User.objects.create_user(username=user_info['login'])
        user.set_password(access_token)
        user.save()

    refresh = RefreshToken.for_user(user)

    response = HttpResponseRedirect(redirect_to=os.getenv("FRONTEND_URL"))
    response.set_cookie('access_token', str(
        refresh.access_token), httponly=True, secure=True, samesite='LAX')
    response.set_cookie('refresh_token', str(
        refresh), httponly=True, secure=True, samesite='LAX')
    return response

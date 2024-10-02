from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import requests
from requests import Response
import os
from django.contrib.auth.models import User

from apps.auth.serializers import OAuth2LoginSerializer


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
        try:
            create_user(response)
        except:
            return JsonResponse({"message": "Could not create user. Please try again."}, status=500)
        return HttpResponseRedirect(redirect_to=os.getenv("FRONTEND_URL"))
    return JsonResponse({"message": "Could not get user access token"}, status=400)


def create_user(user_data: Response):
    access_token = user_data.json()['access_token']
    user_data = requests.get("https://api.github.com/user", headers={
        "Authorization": f"Bearer {access_token}"
    }).json()
    serializer = OAuth2LoginSerializer(data=user_data)
    try:
        serializer.is_valid(raise_exception=True)
    except:
        user = User.objects.create_user(
            username=user_data['login'])
        user.set_password(access_token)
        user.save()

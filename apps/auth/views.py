import json
from urllib.parse import urlencode

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.serializers import LoginSerializer, RegisterSerializer
from apps.user.serializers import UserSerializer
from apps.user.services import google_get_access_token, google_get_user_info


@method_decorator(csrf_protect, name="dispatch")
class SessionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse(data={"isAuthenticated": True})
        else:
            return JsonResponse(data={"isAuthenticated": False})


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            serializer = LoginSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            login(self.request, user)
            serializer = UserSerializer(user)
            return JsonResponse(
                {"success": True, "message": "User successfully logged in"}
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": "User not found. Invalid username or password",
                },
                status=400,
            )


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        error = None
        try:
            serializer = RegisterSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            User.objects.create_user(
                username=serializer.initial_data["username"],
                password=serializer.initial_data["password"],
            )
            return JsonResponse(
                {"success": True, "message": "User successfully created"}, status=201
            )
        except serializers.ValidationError as e:
            error = e.detail["password"][0]
            return JsonResponse({"success": False, "message": str(error)}, status=400)
        except Exception as e:
            error = "User already exists"
            return JsonResponse({"success": False, "message": str(error)}, status=400)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = json.loads(self.request.body)["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        print(request.body)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'https://localhost:3000/login'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        domain = 'https://localhost:8000/'
        # api_uri =
        redirect_uri = 'https://localhost:8000/api/auth/google/login/'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'email': user_data['email'],
            'first_name': user_data.get('givenName', ''),
            'last_name': user_data.get('familyName', ''),
        }

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = User.objects.create_user(**profile_data)

        response = redirect('https://localhost:3000/')
        response = login(self.request, user)

        return response

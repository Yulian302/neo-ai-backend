import json

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.serializers import LoginSerializer, RegisterSerializer, AuthSerializer
from apps.user.serializers import UserSerializer
from apps.user.services import get_user_data
from djangoProject import settings


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
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        auth_serializer = AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)

        validated_data = auth_serializer.validated_data
        user_data = get_user_data(validated_data)

        user = User.objects.get(email=user_data["email"])
        login(request, user)

        return redirect(settings.BASE_APP_URL)

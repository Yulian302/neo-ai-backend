from rest_framework import permissions, status
from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.serializers import LoginSerializer, RegisterSerializer


from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response = JsonResponse({
                "success": True,
                "message": "User successfully logged in",
            })

            response.set_cookie("access_token", str(
                access_token), httponly=True, secure=False, samesite=None)
            response.set_cookie("refresh_token", str(
                refresh), httponly=True, secure=False, samesite=None)
            return response

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "User not found. Invalid username or password",
            }, status=400)


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            return JsonResponse({
                "success": True,
                "message": "User successfully created",
            }, status=201)

        except ValidationError as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": "User already exists"}, status=400)


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

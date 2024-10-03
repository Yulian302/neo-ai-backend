

from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


def verify_token(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return JsonResponse({"detail": "No token provided"}, status=401)

    authentication = JWTAuthentication()
    try:
        validated_token = authentication.get_validated_token(token)
        user = authentication.get_user(validated_token)
        return JsonResponse({"message": "Token is valid", "username": user.username}, status=200)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=401)

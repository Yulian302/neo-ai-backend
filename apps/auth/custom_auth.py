from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if access_token is None:
            return None

        validated_token = self.get_validated_token(access_token)

        try:
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            raise InvalidToken("Invalid token")

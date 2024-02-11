from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfToken(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        csrf_token = get_token(self.request)
        return JsonResponse({"csrftoken": csrf_token})

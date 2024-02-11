from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return JsonResponse(self.request, {"success": True})

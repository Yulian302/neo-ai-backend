from rest_framework import generics, status, permissions
from rest_framework.response import Response

from apps.auth.custom_auth import CookieJWTAuthentication
from apps.user.models import UserNotification
from apps.user.serializers import UserNotificationsSerializer


class UserNotificationDeleteView(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [CookieJWTAuthentication]
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationsSerializer

    def delete(self, request, *args, **kwargs):
        try:
            notification = self.get_object()
            notification.delete()
            return Response(
                {"detail": "Notification deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except UserNotification.DoesNotExist:
            return Response(
                {"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UserNotificationDeleteAllView(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationsSerializer

    def delete(self, request, *args, **kwargs):
        try:
            notifications = self.queryset.filter(user=request.user)
            notifications.delete()
            return Response(
                {"detail": "All notifications deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="profile"
    )
    avatar_url = models.CharField(max_length=255)


class UserNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.TextField()
    success_number = models.IntegerField(default=1)
    # 0 - success
    # 1 - info
    # 2 - warning
    # 3 - error
    created_at = models.DateTimeField(auto_now_add=True)

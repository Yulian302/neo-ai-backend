from django.contrib import admin
from .models import UserProfile, UserNotification


admin.site.register(UserNotification)
admin.site.register(UserProfile)

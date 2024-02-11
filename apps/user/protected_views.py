from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UserNotification


@login_required(login_url="login")
def team(request):
    return render(request, "user/team.jinja2")


def delete_notifications(request):
    if request.method == "POST":
        if "clear_all" in request.POST:
            UserNotification.objects.all().delete()
        else:
            notification_id = request.POST["notification"]
            if notification_id:
                UserNotification.objects.filter(id=notification_id).delete()
        return redirect("settings_notifications")

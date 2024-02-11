from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.apirouter.urls")),
    path("accounts/", include("allauth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    re_path(r"^favicon\.ico$", RedirectView.as_view(url="/static/favicon.ico")),
]

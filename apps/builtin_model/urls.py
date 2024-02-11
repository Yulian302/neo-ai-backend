from django.urls import path, re_path

from apps.builtin_model.views import *

urlpatterns = [
    re_path(r"^$", AiModelViewSet.as_view({"get": "list"})),
    path("<int:pk>/", AiModelViewSet.as_view({"get": "retrieve"})),
    path("<int:pk>/use/", AiModelUsageViewSet.as_view({"post": "use"})),
]

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class AiModelViewSet(ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = AiModelSerializer
    queryset = AiModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        model = get_object_or_404(self.queryset, pk=kwargs["pk"])
        serializer = AiModelDetailsSerializer(model)
        return Response(serializer.data)

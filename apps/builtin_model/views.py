from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from .serializers import *
from .utils.prediction import use_model

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


class AiModelUsageViewSet(ViewSet):
    serializer_class = AiImageUploadSerializer

    @action(detail=False, methods=["post"])
    def use(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            format_, img_str = request.data["image"].split(";base64,")
            ext_ = format_.split("/")[-1]
            model_name = request.data["model_name"]
            prediction_label, infer_time = use_ai_model(model_name, img_str)
            return JsonResponse(
                {"prediction_label": prediction_label, "inference_time": infer_time},
                safe=False,
            )
        except ValidationError as e:
            return JsonResponse({"error": e})
        except Exception as e:
            return JsonResponse({"error": e})


def use_ai_model(model_name: str, base64data):
    model_path = f"/Users/yulianbohomol/PycharmProjects/djangoProject/apps/builtin_model/serialized/{model_name.lower()}.h5"
    pred_, infer_time_ = use_model(
        model_path, model_name=model_name, base64data=base64data
    )
    return pred_, infer_time_

import os.path

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
from .utils.prediction import use_vgg16_model
from .utils.segmentation import use_unet_model

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
    def use(self, request, pk=None, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            format_, img_str = request.data["image"].split(";base64,")
            ext_ = format_.split("/")[-1]
            model_name = AiModel.objects.get(id=pk).name
            models_size = {
                'ClModel': 512,
                'BrainTumorMriSegmentationUnet': 128
            }
            prediction_label, infer_time = use_ai_model(model_name, img_str, img_size=models_size[model_name])
            return JsonResponse(
                {"prediction_label": prediction_label, "inference_time": infer_time},
                safe=False,
            )
        except ValidationError as e:
            return JsonResponse({"error": e})
        except Exception as e:
            return JsonResponse({"error": e})


def use_ai_model(model_name: str, base64data, img_size):
    model_path = os.path.join(settings.BASE_DIR, f'apps/builtin_model/serialized/{model_name}.h5')
    model_params = {
        'ClModel': lambda: use_vgg16_model(model_path, model_name, base64data, img_size),
        'BrainTumorMriSegmentationUnet': lambda: use_unet_model(model_path, base64data, img_size)
    }
    pred_, infer_time_ = model_params[model_name]()
    return pred_, infer_time_

from rest_framework.fields import FileField
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from apps.builtin_model.models import AiModel


class AiModelSerializer(ModelSerializer):
    class Meta:
        model = AiModel
        fields = ["id", "name", "desc_name", "image"]


class AiModelDetailsSerializer(ModelSerializer):
    class Meta:
        model = AiModel
        fields = "__all__"


class AiImageUploadSerializer(Serializer):
    image = CharField()

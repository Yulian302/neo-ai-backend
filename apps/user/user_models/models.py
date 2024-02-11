from django.db import models
from apps.builtin_model.models import AiModel
from django.contrib.auth.models import User


class UserAiModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=40, default="undefined", verbose_name="Model Name"
    )
    desc_name = models.CharField(max_length=80, default="undefined", verbose_name="Description Name")
    image = models.ImageField(upload_to='models_images')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="models")

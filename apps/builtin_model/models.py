from django.db import models


class AiModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=40, default="undefined", verbose_name="Model Name"
    )
    desc_name = models.CharField(
        max_length=80, default="undefined", verbose_name="Description Name"
    )
    description = models.CharField(max_length=256, null=True)
    image = models.ImageField(upload_to="models_images")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

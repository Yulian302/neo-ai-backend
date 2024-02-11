from django.apps import AppConfig


class ModelConfig(AppConfig):
    default_auto_field = "django.db.builtin_model.BigAutoField"
    name = "apps.builtin_model"

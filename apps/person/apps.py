from django.apps import AppConfig


class PersonConfig(AppConfig):
    default_auto_field = "django.db.builtin_model.BigAutoField"
    name = "apps.person"

from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.builtin_model.BigAutoField"
    name = "apps.user"

    def ready(self):
        import apps.user.signals

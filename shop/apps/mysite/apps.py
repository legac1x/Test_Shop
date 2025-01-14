from django.apps import AppConfig # type: ignore


class MysiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mysite'
    verbose_name = 'Магазин'

    def ready(self):
        import apps.mysite.signals

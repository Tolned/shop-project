from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Конфигурация приложения catalog."""

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'catalog'
    verbose_name: str = 'Каталог товаров'
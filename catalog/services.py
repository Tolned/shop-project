"""Сервисные функции для работы с продуктами."""
from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id: int):
    """
    Возвращает список всех продуктов в указанной категории.
    Использует низкоуровневое кэширование с ключом category_{id}.
    TTL = 60 * 15 секунд (15 минут).
    """
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        # Если данных нет в кэше — получаем из БД
        products = list(Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category'))

        # Сохраняем в кэш на 15 минут
        cache.set(cache_key, products, 60 * 15)

    return products
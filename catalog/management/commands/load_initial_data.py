"""
Кастомная команда для очистки базы и загрузки начальных данных.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    """Команда управления для загрузки фикстур."""

    help = 'Очищает базу данных и загружает начальные данные из фикстур'

    def handle(self, *args, **kwargs):
        """
        Основной метод команды.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        self.stdout.write('Очистка базы данных от старых записей...')

        # Сначала удаляем продукты, потом категории (из-за внешних ключей)
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('База очищена!'))
        self.stdout.write('Начинаем загрузку фикстур...')

        # Вызываем стандартную команду loaddata
        call_command('loaddata', 'categories_and_products.json')

        # Выводим итоговый результат
        cat_count = Category.objects.count()
        prod_count = Product.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Загружено категорий: {cat_count}, товаров: {prod_count}'
        ))
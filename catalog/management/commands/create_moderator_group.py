"""Кастомная команда для создания группы модераторов продуктов."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с необходимыми правами'

    def handle(self, *args, **options):
        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует'))

        # Получаем контент-тип модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Находим нужные права
        permissions = Permission.objects.filter(content_type=content_type)

        # Список кодов прав, которые нужно назначить
        required_permissions = [
            'can_unpublish_product',  # Кастомное право
            'delete_product',  # Право на удаление любого продукта
        ]

        for perm_code in required_permissions:
            try:
                perm = permissions.get(codename=perm_code)
                group.permissions.add(perm)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Право "{perm_code}" назначено'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  ✗ Право "{perm_code}" не найдено'))

        self.stdout.write(self.style.SUCCESS(f'\nВ группе "{group.name}" теперь {group.permissions.count()} прав'))
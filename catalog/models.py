"""Модели приложения catalog."""
from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    """Категория продукта."""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт."""
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='catalog/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    # НОВОЕ: поле статуса публикации (Задание 1)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    # НОВОЕ: поле владельца (Задание 2)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        # Кастомное право can_unpublish_product
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})
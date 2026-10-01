from django.db import models


class Category(models.Model):
    """Модель категории товаров."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название категории",
        help_text="Введите название категории"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
        help_text="URL-идентификатор категории"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание категории (необязательно)"
    )

    class Meta:
        """Метаданные модели Category."""
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        """Возвращает строковое представление категории."""
        return self.name


class Product(models.Model):
    """Модель товара."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название товара",
        help_text="Введите название товара"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию товара"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Укажите цену товара"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание товара (необязательно)"
    )
    image = models.ImageField(
        upload_to="products/%Y/%m/%d/",
        blank=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение товара"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        """Метаданные модели Product."""
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        """Возвращает строковое представление товара."""
        return self.name
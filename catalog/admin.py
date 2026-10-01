from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для модели Category."""

    list_display: tuple[str, ...] = ('name', 'slug', 'description')
    prepopulated_fields: dict[str, tuple[str, ...]] = {'slug': ('name',)}
    search_fields: tuple[str, ...] = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для модели Product."""

    list_display: tuple[str, ...] = ('name', 'category', 'price', 'created_at')
    list_filter: tuple[str, ...] = ('category', 'created_at')
    search_fields: tuple[str, ...] = ('name', 'description')
    readonly_fields: tuple[str, ...] = ('created_at', 'updated_at')
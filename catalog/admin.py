"""Админка приложения catalog."""
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для продуктов."""
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'owner')
    list_filter = ('is_published', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ('owner',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'image', 'category'),
        }),
        ('Публикация и владелец', {
            'fields': ('is_published', 'owner'),
        }),
    )
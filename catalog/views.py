"""Контроллеры приложения catalog."""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница — список товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


@method_decorator(cache_page(60 * 5), name='dispatch')  # Кэш на 5 минут
class ProductDetailView(DetailView):
    """Детальная страница товара (с кэшированием)."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerOrModeratorMixin(UserPassesTestMixin):
    """Миксин: доступ только владельцу или модератору."""

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.has_perm('catalog.can_unpublish_product')


class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    """Редактирование товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.has_perm('catalog.delete_product')


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = 'catalog/contacts.html'


from django.shortcuts import render, get_object_or_404
from .services import get_products_by_category


def category_products_view(request, category_id):
    """
    Представление для отображения списка продуктов в указанной категории.
    Использует сервисную функцию с кэшированием.
    """
    from .models import Category
    category = get_object_or_404(Category, pk=category_id)
    products = get_products_by_category(category_id)

    return render(request, 'catalog/category_products.html', {
        'category': category,
        'products': products,
    })
"""Контроллеры приложения catalog."""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница — список товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Детальная страница товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара (только для авторизованных)."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'

    def form_valid(self, form):
        """Автоматически привязываем товар к текущему пользователю."""
        form.instance.owner = self.request.user
        # По умолчанию is_published=False (не опубликован)
        return super().form_valid(form)


class OwnerOrModeratorMixin(UserPassesTestMixin):
    """Миксин: доступ только владельцу или модератору."""

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Владелец ИЛИ пользователь с правом can_unpublish_product (модератор)
        return obj.owner == user or user.has_perm('catalog.can_unpublish_product')


class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    """Редактирование товара (только владелец или модератор)."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара (владелец ИЛИ модератор с правом delete_product)."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Владелец ИЛИ модератор (с правом delete_product)
        return obj.owner == user or user.has_perm('catalog.delete_product')


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = 'catalog/contacts.html'
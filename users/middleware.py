"""Middleware для проверки авторизации."""
from django.shortcuts import redirect
from django.contrib import messages


class LoginRequiredMiddleware:
    """Middleware, требующий авторизации для всех страниц, кроме указанных."""

    def __init__(self, get_response):
        self.get_response = get_response
        # URL-адреса, доступные без авторизации
        self.exempt_urls = [
            '/',                      # ← ДОБАВЛЕНО: главная страница
            '/users/login/',
            '/users/register/',
            '/users/public/',
            '/admin/',
            '/media/',                # ← ДОБАВЛЕНО: для загрузки изображений
            '/static/',               # ← ДОБАВЛЕНО: для статических файлов
        ]

    def __call__(self, request):
        if not any(request.path.startswith(url) for url in self.exempt_urls):
            if not request.user.is_authenticated:
                messages.warning(request, 'Пожалуйста, авторизуйтесь для доступа к этой странице.')
                return redirect('users:login')

        response = self.get_response(request)
        return response
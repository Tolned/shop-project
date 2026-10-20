"""Представления приложения users."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register_view(request):
    """Регистрация пользователя."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Отправка приветственного письма
            send_mail(
                subject='Добро пожаловать в наш магазин!',
                message=f'Здравствуйте, {user.username}!\n\nСпасибо за регистрацию.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Авторизация пользователя."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Неверный email или пароль.')
        else:
            messages.error(request, 'Неверный email или пароль.')
    else:
        form = CustomAuthenticationForm()

    # ВАЖНО: здесь только один .html
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Выход пользователя."""
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')


@login_required
def profile_view(request):
    """Страница профиля (требует авторизации)."""
    return render(request, 'users/profile.html', {'user': request.user})


def public_view(request):
    """Публичная страница (доступна всем)."""
    return render(request, 'users/public.html')
"""Модели приложения users."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с email как USERNAME_FIELD."""

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Введите адрес электронной почты'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        verbose_name='Аватар',
        help_text='Загрузите фото профиля'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Страна',
        help_text='Введите страну проживания'
    )

    # Указываем email как поле для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username обязателен для AbstractUser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
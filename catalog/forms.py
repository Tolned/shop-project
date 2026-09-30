"""Формы приложения catalog."""
from django import forms
from django.core.exceptions import ValidationError

from .models import Product


# Константа со списком запрещённых слов
FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену',
                'step': '0.01',
                'min': '0',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите описание товара',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def _validate_forbidden_words(self, value):
        """Проверка на наличие запрещённых слов в тексте."""
        if value:
            value_lower = value.lower()
            for word in FORBIDDEN_WORDS:
                if word in value_lower:
                    raise ValidationError(
                        f'Поле содержит запрещённое слово: "{word}"'
                    )
        return value

    def clean_name(self):
        """Валидация поля name."""
        name = self.cleaned_data.get('name', '')
        return self._validate_forbidden_words(name)

    def clean_description(self):
        """Валидация поля description."""
        description = self.cleaned_data.get('description', '')
        return self._validate_forbidden_words(description)

    def clean_price(self):
        """Валидация поля price (Задание 2)."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price
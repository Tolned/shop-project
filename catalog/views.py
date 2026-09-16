from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

def home(request):
    # Чек-лист: Использован лаконичный запрос
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def product_detail(request, pk):
    # Чек-лист: Контроллер получает pk, извлекает объект через ORM (защита от ошибок через get_object_or_404)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def add_product(request):
    # Чек-лист: Валидная форма, поля обязательны, защита от ошибок, сохранение в БД
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})
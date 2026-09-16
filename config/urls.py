from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from catalog import views  # <-- Импортируем views из приложения catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'), # Чек-лист: URL вида /products/<int:pk>/, нейминг product_detail
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
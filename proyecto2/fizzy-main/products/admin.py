
from django.contrib import admin
from .models import Product, Category

# Registra el modelo de Producto
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'brand', 'category')  # Campos que quieres mostrar en la lista
    search_fields = ('name', 'brand')  # Habilita la búsqueda por nombre y marca

# Registra el modelo de Categoría
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Campos que quieres mostrar
    search_fields = ('name',)  # Búsqueda por nombre

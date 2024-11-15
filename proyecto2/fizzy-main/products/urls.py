from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductosEnStockAPIView
from . import views
from .views import (
    CategoryViewSet, ProductViewSet, ReviewViewSet, 
    lista_productos, detalle_producto, gestion_productos, crear_producto, editar_producto, eliminar_producto, top_productos_vendidos,productos_mas_comentados, agregar_review, productos_convertidos
)

# Mantén el enrutador para la API REST
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

# Añade las rutas tradicionales de vistas HTML
urlpatterns = [
    path('', include(router.urls)),  # Rutas API
    path('api/productos-en-stock/', ProductosEnStockAPIView.as_view(), name='productos_en_stock_api'),

    # Rutas para usuarios finales
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('productos/top-vendidos/', top_productos_vendidos, name='top_productos_vendidos'),  # Añadir ruta para productos más vendidos
    path('productos/top-comentados/', productos_mas_comentados, name='productos_mas_comentados'),  # Añadir ruta para productos más comentados
    path('productos/<int:product_id>/agregar-review/', agregar_review, name='agregar_review'),
    path('productos/convertidos/', productos_convertidos, name='productos_convertidos'),
    path('productos-aliados/', views.productos_aliados, name='productos_aliados'),
    
    # Rutas para administradores
    path('admin/productos/', gestion_productos, name='gestion_productos'),
    path('admin/productos/new/', crear_producto, name='crear_producto'),
    path('admin/productos/<int:pk>/edit/', editar_producto, name='editar_producto'),
    path('admin/productos/<int:pk>/delete/', eliminar_producto, name='eliminar_producto'),
]

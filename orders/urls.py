from django.urls import path
from .views import generar_factura_pdf

urlpatterns = [
    # Otras rutas de orders
    path('factura/<int:order_id>/', generar_factura_pdf, name='generar_factura_pdf'),
]

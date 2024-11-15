from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Product, Review
from .forms import ProductoForm, ReviewForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import CurrencyService
import requests
from decimal import Decimal  # Importar Decimal para manejar cálculos precisos


class ProductosEnStockAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """Devuelve una lista de productos en stock."""
        productos_en_stock = Product.objects.filter(stock__gt=0)  # Productos con stock > 0
        serializer = ProductSerializer(productos_en_stock, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Vista para que los usuarios vean la lista de productos // Busqueda por nombre
@login_required
def lista_productos(request):
    query = request.GET.get('q')
    if query:
        productos = Product.objects.filter(name__icontains=query)
    else:
        productos = Product.objects.all()
    return render(request, 'users/product_list.html', {'productos': productos})

# Vista para que los usuarios vean los detalles de un producto
@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

@login_required #Productos mas vendidos
def top_productos_vendidos(request):
    productos = Product.objects.order_by('-ventas')[:3]
    return render(request, 'users/top_productos.html', {'productos': productos})

@login_required
def productos_mas_comentados(request): #productos con mas reviews
    productos = Product.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')[:4]
    return render(request, 'users/top_comentados.html', {'productos': productos})


@login_required
def agregar_review(request, product_id):
    producto = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = producto  # Asociar la review al producto
            review.user = request.user  # Asociar la review al usuario
            review.save()
            return redirect('detalle_producto', pk=producto.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'productos/agregar_review.html', {'form': form, 'producto': producto})





# Verificación para asegurarse de que el usuario es administrador
def es_admin(user):
    return user.is_superuser or user.role == 'admin'

@user_passes_test(es_admin)
def gestion_productos(request):
    productos = Product.objects.all()
    return render(request, 'admin/gestion_productos.html', {'productos': productos})

@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    else:
        form = ProductoForm()
    return render(request, 'admin/crear_producto.html', {'form': form})

@user_passes_test(es_admin)
def editar_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'admin/editar_producto.html', {'form': form})

@user_passes_test(es_admin)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('gestion_productos')
    return render(request, 'admin/eliminar_producto.html', {'producto': producto})


def productos_convertidos(request):
    """Vista para mostrar productos con precios convertidos."""
    moneda_destino = request.GET.get('moneda', 'EUR')  # Moneda por defecto: EUR
    tasa_cambio = CurrencyService.obtener_tasa_cambio(moneda_destino)
    productos = Product.objects.all()

    # Si no se puede obtener la tasa de cambio, devuelve un mensaje de error
    if tasa_cambio is None:
        return render(request, 'productos/lista_productos.html', {
            'error': f"No se pudo obtener la tasa de cambio para {moneda_destino}.",
            'productos': productos,
        })

     # Convertir precios a la moneda deseada
    tasa_cambio_decimal = Decimal(str(tasa_cambio))
    for producto in productos:
        producto.precio_convertido = round(producto.price * tasa_cambio_decimal, 2)

    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'moneda_destino': moneda_destino,
        'tasa_cambio': tasa_cambio,
    })


def productos_aliados(request):
    try:
        # Cambia esta URL a la del equipo del que vas a consumir datos
        response = requests.get("http://url_del_equipo_2/api/products/stock/")
        response.raise_for_status()  # Verifica si hubo errores en la solicitud
        productos_aliados = response.json()  # Parsear el JSON de la respuesta
    except requests.exceptions.RequestException as e:
        productos_aliados = []
        print("Error al conectar con el servicio del equipo aliado:", e)

    return render(request, 'productos/productos_aliados.html', {
        'productos_aliados': productos_aliados
    })

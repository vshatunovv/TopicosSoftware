from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'brand', 'images', 'category', 'ventas', 'product_url']

    def get_product_url(self, obj):
        """Generar enlace directo a la visualización del producto."""
        request = self.context.get('request')  # Acceder al contexto de la solicitud
        return request.build_absolute_uri(f'/productos/{obj.id}/')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

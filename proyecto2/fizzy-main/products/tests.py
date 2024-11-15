from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="A category for testing"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="A product for testing",
            price=99.99,
            stock=10,
            brand="Test Brand",
            images=["https://example.com/image1.jpg"],
            category=self.category
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.stock, 10)

    def test_negative_stock(self):
        with self.assertRaises(ValidationError):
            product = Product(
                name="Invalid Product",
                description="A product with invalid stock",
                price=99.99,
                stock=-5,  # Valor negativo
                brand="Test Brand",
                images=["https://example.com/image1.jpg"],
                category=self.category
            )
            product.full_clean()  # Llama a la validación explícitamente

    def test_negative_sales(self):
        with self.assertRaises(ValidationError):
            product = Product(
                name="Invalid Product",
                description="A product with invalid sales",
                price=99.99,
                stock=10,
                ventas=-1,  # Ventas negativas
                brand="Test Brand",
                images=["https://example.com/image1.jpg"],
                category=self.category
            )
            product.full_clean()  # Llama a la validación explícitamente

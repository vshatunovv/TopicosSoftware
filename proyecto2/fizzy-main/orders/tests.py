from django.test import TestCase
from users.models import CustomUser
from products.models import Product, Category
from orders.models import Order, OrderItem

class OrderModelTest(TestCase):
    def setUp(self):
        # Crear una categoría para los productos
        self.category = Category.objects.create(
            name="Test Category",
            description="A category for testing"
        )

        # Crear un usuario de prueba
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        # Crear un producto asociado a la categoría
        self.product = Product.objects.create(
            name="Test Product",
            description="A product for testing",
            price=10.00,
            stock=100,
            brand="Test Brand",
            images=["https://example.com/image1.jpg"],
            category=self.category  # Asignar la categoría
        )

        # Crear una orden
        self.order = Order.objects.create(
            user=self.user,
            status="pending",
            total=0  # Inicialmente en 0
        )

        # Crear un ítem de orden
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            subtotal=20.00  # 2 productos a $10 cada uno
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.status, "pending")
        self.assertEqual(self.order.total, 0)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product.name, "Test Product")
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.subtotal, 20.00)

    def test_order_total_calculation(self):
    #Prueba que el total de la orden se calcula correctamente.#
        total = sum(item.subtotal for item in self.order.items.all())  # Accede a items desde Order
        self.order.total = total
        self.order.save()
        self.assertEqual(self.order.total, 20.00)


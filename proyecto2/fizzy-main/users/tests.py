from django.test import TestCase
from users.models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        # Crear un usuario estándar
        self.user = CustomUser.objects.create_user(
            email="user@example.com",
            username="testuser",
            password="password123",
            role="customer"
        )

        # Crear un superusuario
        self.superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="adminuser",
            password="adminpassword",
            role="admin"
        )

    def test_user_creation(self):
        """Prueba que un usuario estándar se crea correctamente."""
        self.assertEqual(self.user.email, "user@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.role, "customer")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_creation(self):
        """Prueba que un superusuario se crea correctamente."""
        self.assertEqual(self.superuser.email, "admin@example.com")
        self.assertEqual(self.superuser.username, "adminuser")
        self.assertTrue(self.superuser.check_password("adminpassword"))
        self.assertEqual(self.superuser.role, "admin")
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def test_user_without_email(self):
        """Prueba que no se puede crear un usuario sin email."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="",
                username="nouser",
                password="password123",
                role="customer"
            )

    def test_superuser_defaults(self):
        """Prueba que un superusuario tiene los valores predeterminados is_staff e is_superuser."""
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

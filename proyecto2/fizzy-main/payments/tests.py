from django.test import TestCase
from .pago_cheque import PagoConCheque
from .pago_tarjeta import PagoConTarjeta

class PagoTests(TestCase):
    def test_pago_cheque_valido(self):
        """Prueba que el pago con cheque se procese correctamente para un monto válido"""
        pago = PagoConCheque()
        resultado = pago.procesar_pago(100)
        self.assertEqual(resultado, "Pago procesado con cheque por 100")
    
    def test_pago_tarjeta_valido(self):
        """Prueba que el pago con tarjeta se procese correctamente para un monto válido"""
        pago = PagoConTarjeta()
        resultado = pago.procesar_pago(100)
        self.assertEqual(resultado, "Pago procesado con tarjeta por 100")

    def test_pago_cheque_monto_negativo(self):
        """Prueba que el pago con cheque falle para montos negativos"""
        pago = PagoConCheque()
        with self.assertRaises(ValueError):
            pago.procesar_pago(-50)
    
    def test_pago_tarjeta_monto_negativo(self):
        """Prueba que el pago con tarjeta falle para montos negativos"""
        pago = PagoConTarjeta()
        with self.assertRaises(ValueError):
            pago.procesar_pago(-50)
    
    def test_pago_tarjeta_saldo_insuficiente(self):
        """Prueba que el pago con tarjeta falle si el saldo del usuario es insuficiente"""
        pago = PagoConTarjeta()
        # Imaginemos que el saldo del usuario es 50
        resultado = pago.procesar_pago(100, saldo_usuario=50)
        self.assertEqual(resultado, "Saldo insuficiente para realizar el pago")

    def test_pago_tarjeta_saldo_suficiente(self):
        """Prueba que el pago con tarjeta se procese si el saldo del usuario es suficiente"""
        pago = PagoConTarjeta()
        # Imaginemos que el saldo del usuario es 200
        resultado = pago.procesar_pago(100, saldo_usuario=200)
        self.assertEqual(resultado, "Pago procesado con tarjeta por 100")

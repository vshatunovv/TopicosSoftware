# pago_tarjeta.py
class PagoConTarjeta:
    def procesar_pago(self, monto, saldo_usuario=None):
        if monto < 0:
            raise ValueError("El monto no puede ser negativo")
        if saldo_usuario is not None and saldo_usuario < monto:
            return "Saldo insuficiente para realizar el pago"
        return f"Pago procesado con tarjeta por {monto}"

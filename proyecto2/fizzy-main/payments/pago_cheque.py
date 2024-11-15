
class PagoConCheque:
    def procesar_pago(self, monto):
        if monto < 0:
            raise ValueError("El monto no puede ser negativo")
        print(f"Procesando pago de {monto} con cheque.")
        return f"Pago procesado con cheque por {monto}"

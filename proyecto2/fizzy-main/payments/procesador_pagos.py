from django.shortcuts import render
from payments.pago_cheque import PagoConCheque

class ProcesadorDePagos:
    def __init__(self, metodo_pago):
        # La clase espera un objeto que implemente MetodoPagoInterface
        self.metodo_pago = metodo_pago

    def realizar_pago(self, monto):
        # Llama al método de procesar_pago de la clase pasada en metodo_pago
        self.metodo_pago.procesar_pago(monto)

def procesar_pago_view(request):
    if request.method == "POST":
        monto = float(request.POST.get("monto"))
        metodo_pago = PagoConCheque()  # Puedes cambiar este método por otro en el futuro

        try:
            resultado = metodo_pago.procesar_pago(monto)
            mensaje = resultado
        except ValueError as e:
            mensaje = str(e)

        return render(request, "procesar_pago.html", {"mensaje": mensaje})

    return render(request, "procesar_pago.html")

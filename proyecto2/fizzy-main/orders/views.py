from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # Importamos la librería para generar PDFs
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def generar_factura_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Permitir acceso solo si el usuario es el propietario de la orden o si es superusuario
    if request.user != order.user and not request.user.is_superuser:
        return HttpResponse("No tienes permiso para ver esta factura.", status=403)

    # Obtener los items de la orden
    order_items = order.order_items.all()

    # Cargar el template de la factura
    template = get_template('orders/factura.html')
    context = {
        'order': order,
        'order_items': order_items,  # Pasamos los items de la orden al template
    }
    
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{order.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}')

    return response


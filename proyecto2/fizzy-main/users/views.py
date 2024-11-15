from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistroUsuarioForm  # Importa tu formulario personalizado
from django.utils.translation import gettext as _

def register(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('home')  # Redirige a la página principal u otra página después del registro
    else:
        form = RegistroUsuarioForm()  # Usa el formulario personalizado
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    # Agregar un mensaje de éxito
    messages.success(request, '¡Bienvenido!')
    # Lógica de inicio de sesión

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

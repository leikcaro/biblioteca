from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Autor, Cliente, Prestamo
from django.contrib.auth.views import LoginView, LogoutView #, PasswordChangeView

#Home
def home(request):
    return render(request, 'home.html')

#####Autenticación#####

#Registro

def register(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # Crear al cliente asociado
            Cliente.objects.create(
                user=user,
                rut=form.cleaned_data['rut'],
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email']
            )

            # Autenticar y redirigir
            login(request, user)
            return redirect('home')  
    else:
        form = ClienteRegistroForm()
    return render(request, 'registration/register.html', {'form': form})

#Vistas de Autenticación
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
    
# Vistas para Autor
class AutorListView(ListView):
    model = Autor
    template_name = 'autor/autor_list.html'
    context_object_name = 'autores'

class AutorCreateView(CreateView):
    model = Autor
    template_name = 'autor/autor_form.html'
    fields = ['nombre', 'especialidad']
    success_url = reverse_lazy('autor_list')

class AutorUpdateView(UpdateView):
    model = Autor
    template_name = 'autor/autor_update.html'
    fields = ['nombre', 'especialidad']
    success_url = reverse_lazy('autor_list')


class AutorDeleteView(DeleteView):
    model = Autor
    template_name = 'autor/autor_confirm_delete.html'
    success_url = reverse_lazy('autor_list')

# Vistas para Prestamo
class PrestamoListView(ListView):
    model = Prestamo
    template_name = 'prestamo/prestamo_list.html'
    context_object_name = 'prestamos'

class PrestamoCreateView(CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo/prestamo_create.html'
    success_url = reverse_lazy('prestamo_list')

    # Validación de copias y prestamos duplicados (para el final)
    def form_valid(self, form):
        """
        En caso de que el método save() del modelo lance ValidationError
        (por falta de copias o préstamo duplicado), capturamos la excepción
        y mostramos el error en el formulario.
        """
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)  # Muestra el error arriba del formulario
            return self.form_invalid(form)

class PrestamoUpdateView(UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo/prestamo_update.html'
    success_url = reverse_lazy('prestamo_list')

    #IDEM Validación para el final
    def form_valid(self, form):
        # Mismo manejo de validación que en CreateView
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class PrestamoDeleteView(DeleteView):
    model = Prestamo
    template_name = 'prestamo/prestamo_confirm_delete.html'
    success_url = reverse_lazy('prestamo_list')
    
    
#Mis prestamos:

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Prestamo

class MisPrestamosListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'prestamo/mis-prestamos.html'
    context_object_name = 'prestamos'

    def get_queryset(self):
        """
        Devuelve la lista de préstamos solamente para el cliente
        asociado al usuario que está logueado.
        """
        user = self.request.user
        # Dado que en Cliente tenemos un OneToOne con User,
        # podemos obtener el objeto cliente con user.cliente
        return Prestamo.objects.filter(cliente__user=user)
from django import forms
from django.contrib.auth.models import User
from .models import *

class ClienteRegistroForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'email']
        widgets = {'password': forms.PasswordInput}
        
    
    # Ordenar los campos
    field_order = ['username', 'password', 'rut', 'nombre', 'email']
    
class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['cliente', 'libro']
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Autor, Libro, Cliente, Prestamo

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad')


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'tema', 'copias', 'autor')
    list_filter = ('tema', 'autor')
    search_fields = ('titulo', 'codigo')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'email')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'libro', 'fecha_prestamo')

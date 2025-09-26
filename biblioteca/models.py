from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tema = models.CharField(max_length=100)
    copias = models.PositiveIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")

    def __str__(self):
        return self.titulo


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="prestamos")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="prestamos")
    fecha_prestamo = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Validar que haya copias disponibles
        if self.libro.copias <= 0:
            raise ValidationError("No hay copias disponibles de este libro.")
        
        # Validar que el cliente no haya pedido el mismo libro antes
        if Prestamo.objects.filter(cliente=self.cliente, libro=self.libro).exists():
            raise ValidationError("El cliente ya tiene este libro prestado.")
        
        # Reducir la cantidad de copias disponibles
        self.libro.copias -= 1
        self.libro.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Al eliminar el préstamo, se incrementa la cantidad de copias disponibles
        self.libro.copias += 1
        self.libro.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.libro}"


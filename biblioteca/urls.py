from django.urls import path
from .views import *

urlpatterns = [
    #URL de Home
    path('', home, name='home'),
    
    #URLs de Autenticación
    path("register/", register, name="register"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # URLs para Autor
    path('autores/', AutorListView.as_view(), name='autor_list'),
    path('autores/crear/', AutorCreateView.as_view(), name='autor_create'),
    path('autores/<int:pk>/editar/', AutorUpdateView.as_view(), name='autor_update'),
    path('autores/<int:pk>/eliminar/', AutorDeleteView.as_view(), name='autor_delete'),
    
    # URLs para Prestamo
    path('prestamos/', PrestamoListView.as_view(), name='prestamo_list'),
    path('prestamos/crear/', PrestamoCreateView.as_view(), name='prestamo_create'),
    path('prestamos/<int:pk>/editar/', PrestamoUpdateView.as_view(), name='prestamo_update'),
    path('prestamos/<int:pk>/devolucion/', PrestamoDeleteView.as_view(), name='prestamo_delete'),
    path('mis-prestamos/', MisPrestamosListView.as_view(), name='mis_prestamos'),
]

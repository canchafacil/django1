# reservas/models.py
from django.db import models
from decimal import Decimal

class Reserva(models.Model):
    nombre   = models.CharField(max_length=100)
    correo   = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    fecha    = models.DateField()
    hora     = models.TimeField()
    cancha   = models.CharField(max_length=100)
    duracion = models.CharField(max_length=20)  # ej. "60 min", "2 horas"
    estado   = models.CharField(max_length=20, default='Pendiente')
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)  # Nuevo
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nuevo
    numero_factura = models.CharField(max_length=20, blank=True, null=True)  # Nuevo, opcional

    def __str__(self):
        return f"{self.nombre} - {self.cancha} - {self.fecha}"

    def duracion_minutos(self):
        """Convierte 'duracion' (ej. '60 min', '2 horas') a minutos enteros."""
        texto = self.duracion.lower().strip()
        if 'min' in texto:
            return int(texto.replace('min', '').strip())
        elif 'hora' in texto:
            horas = float(texto.replace('horas', '').replace('hora', '').strip())
            return int(horas * 60)
        else:
            # Intenta extraer número si es solo dígitos
            try:
                return int(texto)
            except:
                return 60  # valor por defecto

    def precio_por_hora(self):
        """Define el precio por hora según la cancha (puedes poner tus precios)."""
        precios = {
            'Cancha A': 50000,
            'Cancha B': 60000,
            'Cancha C': 70000,
            # Agrega más según tu proyecto
        }
        return precios.get(self.cancha, 50000)  # default

    def calcular_total(self):
        """Calcula el total basado en duración y precio por hora."""
        minutos = self.duracion_minutos()
        horas = Decimal(minutos) / 60
        precio_hora = Decimal(self.precio_por_hora())
        return precio_hora * horas
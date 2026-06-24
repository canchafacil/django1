# En reservas/models.py verifica que el modelo tenga el campo estado.
# Si no lo tiene, agrégalo así:

from django.db import models

class Reserva(models.Model):
    nombre   = models.CharField(max_length=100)
    correo   = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    fecha    = models.DateField()
    hora     = models.TimeField()
    cancha   = models.CharField(max_length=100)
    duracion = models.CharField(max_length=20)
    estado   = models.CharField(max_length=20, default='Pendiente')  # ← este campo

    def __str__(self):
        return f"{self.nombre} - {self.cancha} - {self.fecha}"


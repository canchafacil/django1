from django.db import models

class Cancha(models.Model):

    TIPOS = [
        ('Fútbol 5', 'Fútbol 5'),
        ('Fútbol 7', 'Fútbol 7'),
        ('Fútbol 11', 'Fútbol 11'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='canchas/')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
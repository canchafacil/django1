from django.db import models

class Usuario(models.Model):

    ROLES = [
        ('SUPERADMIN', 'Super Administrador'),
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    rol = models.CharField(
        max_length=15,
        choices=ROLES
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} ({self.rol})"
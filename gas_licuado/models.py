from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Solicitud(models.Model):
    ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
    ('expirada', 'Expirada'),
]

    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    comuna = models.CharField(max_length=30)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def expiro(self):
        if self.fecha_aceptacion:
            return timezone.now() > self.fecha_aceptacion + timezone.timedelta(days=30)
        return False
    
    def save(self, *args, **kwargs):
        if self.expiro():
            self.estado = 'expirada' 
        super(Solicitud, self).save(*args, **kwargs)

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        if nuevo_estado == 'aceptada':
            self.fecha_aceptacion = timezone.now() 
        else:
            self.fecha_aceptacion = None  
        self.save()
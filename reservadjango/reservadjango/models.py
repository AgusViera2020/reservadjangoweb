from django.db import models
from datetime import datetime, timedelta
from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length = 30)
    precio = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    imagen = models.ImageField(upload_to='media/servicios/', default='', blank=True)
    #SALES
    descuento = models.BooleanField(default=False)
    precio_descuento =models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length = 50,null=False)
    servicio = models.CharField(max_length = 30, null=False)
    fecha = models.DateTimeField(null=False)
    hora = models.TimeField(null=False)
    contacto = models.IntegerField(default='', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}, {self.servicio}, {str(self.fecha)}, {str(self.hora)}"
    
    def reservas_mes():
        return Reserva.objects.filter(fecha__gt = datetime.now()-timedelta(days=30))
    





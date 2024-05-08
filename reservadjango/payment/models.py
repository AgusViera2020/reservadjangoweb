from django.db import models
from accounts.models import CustomUser
from reservadjango.models import Servicio
from django.db.models.signals import post_save

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    shipping_nombre = models.CharField(max_length=255)
    shipping_email = models.EmailField(max_length=255)
    shipping_cedula = models.CharField(max_length=255)
    shipping_direccion = models.CharField(max_length=255)
    shipping_ciudad = models.CharField(max_length=255) 

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
def create_shipping_address (sender, instance, created, **kwargs):
    if created:
        user_shipping_address = ShippingAddress(user=instance)
        user_shipping_address.save()
post_save.connect(create_shipping_address, sender=CustomUser)

    

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=15000)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Orden - {str(self.id)}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveBigIntegerField(default=1)
    precio = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'Order Item - {str(self.id)} -{str(self.order)}'

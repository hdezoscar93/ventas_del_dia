from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Venta(models.Model):
    nombre_producto = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Campos sugeridos extra:
    metodo_pago = models.CharField(
        max_length=50,
        choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia')],
        default='efectivo'
    )
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    notas = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Si precio_unitario está definido, calcula total
        self.total = self.cantidad * (self.precio_unitario or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_producto} - {self.total} ({self.fecha_registro.date()})"

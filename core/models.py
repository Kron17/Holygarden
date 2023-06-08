from django.db import models

# Create your models here.

#ES DONDE SE CREAN LAS TABLAS
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length = 50)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):

    nombre = models.CharField(max_length = 50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length = 250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    vencimiento = models.DateField()
    imagen = models.ImageField(null=True, blank=True)
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre

class ItemsCarrito(models.Model):
    NombreProducto = models.CharField(max_length=40)
    PrecioProducto = models.IntegerField()
    imagen = models.ImageField(upload_to="items_carrito", null=True)

    def __str__(self):
        return self.NombreProducto
    
    class Meta:
        db_table = "db_items_carrito"
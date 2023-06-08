from django.contrib import admin
from .models import *

# Register your models here.

# DEJA EN MODO TABLA LA VISUALIZACION EN EL ADMIN
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo', 'vigente', 'vencimiento']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['tipo', 'precio']
    list_editable = ['precio','stock','descripcion','tipo','vigente', 'vencimiento']

class CarritoAdmin(admin.ModelAdmin):
    list_display = ['NombreProducto','PrecioProducto']
    search_fields = ['NombreProducto']
    list_per_page = 10
    list_filter = ['PrecioProducto']

admin.site.register(TipoProducto)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(ItemsCarrito, CarritoAdmin)
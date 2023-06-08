from django.urls import path, include
from .views import *
from rest_framework import routers

#rutas del API tienen rutas propias

router = routers.DefaultRouter()
router.register('productos', ProductoViewset)
router.register('tipoproductos', TipoProductoViewset)

urlpatterns = [
    #api
    path('api/', include(router.urls)),
    #RUTAS
    path('', index, name="index"),
    path('base/', base, name="base"),
    path('product/', product, name="productos"),
    path('contacto/', contacto, name="contacto"),
    path('registro/', registro, name="registro"),
    path('seguimiento/', seguimiento, name="seguimiento"),
    path('compra/', compra, name="compra"),
    path('aprobado/', aprobado, name="aprobado"),
    path('seguimientoCompra/', seguimientoCompra, name="seguimientoCompra"),
    path('indexapi', indexapi, name="indexapi"),

    #CRUD
    path('add/', add, name='add'),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', delete, name="delete"),
    
]
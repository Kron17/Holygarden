from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .serializers import *
from rest_framework import viewsets
import requests

#NOS PERMITE MOSTRAR LA INFO
class ProductoViewset(viewsets.ModelViewSet):
    #para poder filtrar queryset = Producto.objects.filter(tipo=1)
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class TipoProductoViewset(viewsets.ModelViewSet):
    #para poder filtrar queryset = Producto.objects.filter(tipo=1)
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer

# Create your views here.
def index(request):
    productosAll = Producto.objects.all() #SELECT * FROM producto
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    
    try:
        paginator = Paginator(productosAll, 4)
        productosAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productosAll,
        'paginator': paginator
    }

    if request.method == 'POST':
        carrito = ItemsCarrito()
        carrito.NombreProducto = request.POST.get('NombreProducto')
        carrito.PrecioProducto = request.POST.get('PrecioProducto')
        carrito.imagen = request.POST.get('imagenProducto')
        carrito.save()
        
    return render(request, 'core/index.html', data)

def base(request):
    respuesta = requests.get('https://mindicador.cl/api').json()

  
    
    
    data = {
        'monedas': respuesta,
         }
    
    return render(request, 'core/base.html', data)

def product(request):
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    productos = respuesta.json()
    #productosAll = Producto.objects.all() #SELECT * FROM producto
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    
    try:
        paginator = Paginator(productos, 8)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productos,
        'paginator': paginator
    }
    
    if request.method == 'POST':
        carrito = ItemsCarrito()
        carrito.NombreProducto = request.POST.get('NombreProducto')
        carrito.PrecioProducto = request.POST.get('PrecioProducto')
        carrito.imagen = request.POST.get('imagenProducto')
        carrito.save()

    return render(request, 'core/product.html', data)

@login_required
def seguimiento(request):
    return render(request, 'core/seguimiento.html')

def seguimientoCompra(request):
    return render(request, 'core/seguimientoCompra.html')

def contacto(request):
    return render(request, 'core/contacto.html')

##def usuario(request):
    ##return render(request, 'registration/usuario.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirige a la página de inicio después del registro exitoso
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def compra(request):
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    carrito = ItemsCarrito.objects.all()
    total_price_without_discount = sum(item.PrecioProducto for item in carrito)
    
    total_price_with_discount = total_price_without_discount
    if request.user.is_authenticated:
        total_price_with_discount *= 0.95

    total_price_without_discount = int(total_price_without_discount)  # Convertir el precio sin descuento a entero
    total_price_with_discount = int(total_price_with_discount)  # Convertir el precio con descuento a entero
    discount_amount = total_price_without_discount - total_price_with_discount
    valor_total = total_price_with_discount/valor_usd

    datos = {
        ##para redondear dolares es round(total,2)solo 2 decimales
        'ListaCarrito': carrito,
        'total_price_without_discount': total_price_without_discount,
        'valor_total': round(valor_total,2),
        'discount_amount': discount_amount,
        'total_price_with_discount': total_price_with_discount
    }

    return render(request, 'core/compra.html', datos)


def aprobado(request):
    carrito = ItemsCarrito.objects.all()
    carrito.delete()

    return render(request, 'core/aprobado.html')

######################## CRUD ########################
@login_required
def add(request):
    data ={
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) #OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() #INSERT INTO...
            #data['msj'] = "Producto guardado correctamente"
            messages.success(request, "Producto almacenado correctamente")

    return render(request, 'core/add-product.html', data)

@login_required
def update(request, id):
    producto = Producto.objects.get(id=id) #OBTIENE UN PRODUCTO POR EL ID
    data ={
        'form' : ProductoForm(instance=producto) #CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, instance=producto, files=request.FILES) #OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() #INSERT INTO...
            #data['msj'] = "Producto actualizado correctamente"
            messages.success(request, "Producto almacenado correctamente")
            data['form'] = formulario #CAGRA LA NUEVA INFO EN EL FORMULARIO
            
    return render(request, 'core/update-product.html', data)

@login_required
def delete(request, id):
    producto = Producto.objects.get(id=id) #OBTIENE UN PRODUCTO POR EL ID
    producto.delete()
    
    return redirect(to = 'index')

def indexapi(request):
    #obtiene productos api
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api')
    #apis mas complejas con arreglos
    respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
    #Transformar JSON
    productos = respuesta.json()
    monedas = respuesta2.json()
    #utilizamos 2 variables para las apis mas coplejas
    envolvente = respuesta3.json()
    personajes = envolvente['results']

    data = {
        'listado': productos,
        'monedas': monedas,
        'personajes': personajes,
        
    }

        
    return render(request, 'core/indexapi.html', data)

######################################################


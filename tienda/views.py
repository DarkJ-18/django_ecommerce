import django.contrib
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import *
from .utils import *
from .templatetags.custom_filters import *


def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        usuario = Usuario.objects.filter(correo=correo, contrasena=contrasena).first()
        if usuario:
            request.session['pista'] = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol
            }
            if usuario.rol == 1:
                return redirect('administrador')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')
    else:
        return render(request, 'admin/login_admin.html')
    
def logout(request):
    try:
        del request.session['pista']
        return redirect('index')
    except:
        messages.error(request, 'Ocurrio un error')
        return redirect('index')

def index(request):
    q = Producto.objects.all()
    context = {'data': q}
    return render(request, 'tienda/index.html', context)

@session_rol_permission(1)
def administrador(request):
    q = Producto.objects.all()
    context = {'data': q}
    return render(request, 'admin/index_admin.html', context)

def listar_productos(request):
    q = Producto.objects.all()
    context = {'data': q}
    return render(request, 'admin/productos/listar_productos.html', context)

@session_rol_permission(1)
def agregar_producto(request):
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio_original = request.POST.get("precio_original", "0")
        descuento = request.POST.get("descuento", "0")
        en_oferta = request.POST.get("en_oferta") == "on"
        stock = request.POST.get("stock")
        categoria = request.POST.get("categoria")
        color = request.POST.get("color")
        imagenes = request.FILES.getlist("imagenes")
        try:
            if len(imagenes) > 5:
                raise Exception("No se pueden agregar más de 5 imágenes")
            formatos_permitidos = ['image/png', 'image/jpg', 'image/jpeg', "image/webp"]
            for imagen in imagenes:
                if imagen.content_type not in formatos_permitidos:
                    raise ValidationError(f"Formato no permitido: {imagen.content_type}. Solo se aceptan JPEG, PNG, GIF o WEBP.")
            # Crear el producto
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio_original=Decimal(precio_original),
                descuento=Decimal(descuento),
                en_oferta=en_oferta,
                stock=stock,
                categoria=int(categoria),
                color=color,
            )
            producto.save()
            # Guardar imágenes
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)
            messages.success(request, 'Producto agregado correctamente')
        except ValidationError as ve:
            messages.error(request, f"Error de validacion: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('administrador')
    else:
        user = request.session.get("pista")
        categorias = Producto.CATEGORIAS
        return render(request, "admin/productos/agregar_producto.html", {
            'user': user,
            'categorias': categorias,
        })


@session_rol_permission(1)
def editar_producto(request, id_producto):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio_original = request.POST.get("precio_original")
        descuento = request.POST.get("descuento", "0")
        en_oferta = request.POST.get("en_oferta") == "on"
        stock = request.POST.get("stock")
        categoria = request.POST.get("categoria")
        color = request.POST.get("color")
        imagenes = request.FILES.getlist("imagenes")
        try:
            # Obtener el producto a editar
            producto = Producto.objects.get(pk=id_producto)
            # Actualizar los campos del producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_original = Decimal(precio_original) if precio_original else Decimal(0)
            producto.descuento = Decimal(descuento) if descuento else Decimal(0)
            producto.en_oferta = en_oferta
            producto.stock = stock
            producto.categoria = categoria
            producto.color = color
            producto.save()
            # Guardar las nuevas imágenes asociadas al producto
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto actualizado correctamente!")            
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('listar_productos')
    else:
        try:
            producto = Producto.objects.get(pk=id_producto)
            categorias = Producto.CATEGORIAS
            return render(request, "admin/productos/editar_producto.html", {
                "dato": producto,
                "categorias": categorias
            })
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
            return redirect('listar_productos')

@session_rol_permission(1)
def eliminar_producto(request, id_producto):
    try:
        q: Producto = Producto.objects.get(id=id_producto)
        q.delete()
        messages.success(request, 'Producto eliminado correctamente')
    except Producto.DoesNotExist:
        messages.error(request, 'Producto no encontrado')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('listar_productos')

def detalle_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    rango_cantidad = range(1, producto.stock + 1)  # Generar el rango basado en el stock
    return render(request, 'admin/productos/detalle_producto.html', {
        'producto': producto,
        'rango_cantidad': rango_cantidad
    })

def productos_por_categoria(request, categoria):
    try:
        # Convertir el valor de categoria a entero
        categoria = int(categoria)
        productos = Producto.objects.filter(categoria=categoria)
        # Obtener el nombre de la categoría
        categoria_nombre = dict(Producto.CATEGORIAS).get(categoria, "Categoría desconocida")
    except ValueError:
        # Si no es un entero, mostrar categoría desconocida
        productos = []

    contexto = {'productos': productos, 'categoria': categoria_nombre}
    return render(request, 'admin/productos/productos_por_categoria.html', contexto)


# ---------------------------------------------
    ## Carrito de compras
# ---------------------------------------------

def obtener_carrito(request):
    if request.user.is_authenticated:
        # Recuperar el carrito del usuario autenticado
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Usar un carrito basado en cookies para usuarios no autenticados
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id).first()
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    return carrito


def agregar_carrito(request, id_producto):
    carrito = obtener_carrito(request)
    producto = get_object_or_404(Producto, id=id_producto)
    cantidad = int(request.POST.get('cantidad', 1))

    # Buscar si el producto ya está en el carrito
    elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        elemento.cantidad += cantidad  # Incrementar la cantidad si ya existe
    else:
        elemento.cantidad = cantidad  # Establecer la cantidad si es un nuevo elemento
    elemento.save()

    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect('carrito')

def carrito(request):
    carrito = obtener_carrito(request)
    elementos = carrito.elementos.all()  # Obtener todos los elementos del carrito
    total = carrito.total()  # Calcular el total del carrito

    contexto = {
        'elementos': elementos,
        'total': total,
    }
    return render(request, 'tienda/carrito.html', contexto)


def eliminar_del_carrito(request, id_elemento):
    elemento = get_object_or_404(ElementoCarrito, id=id_elemento)
    elemento.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('carrito')



def actualizar_carrito(request, id_elemento):
    if request.method == 'POST':
        elemento = get_object_or_404(ElementoCarrito, id=id_elemento)
        nueva_cantidad = int(request.POST.get('cantidad', 1))

        if nueva_cantidad > elemento.producto.stock:
            return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)

        if nueva_cantidad > 0:
            elemento.cantidad = nueva_cantidad
            elemento.save()
            return JsonResponse({
                'subtotal': elemento.subtotal(),
                'total': elemento.carrito.total()
            })
        else:
            elemento.delete()
            return JsonResponse({
                'subtotal': 0,
                'total': elemento.carrito.total()
            })
    return JsonResponse({'error': 'Método no permitido'}, status=405)
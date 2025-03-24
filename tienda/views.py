from django.shortcuts import render, redirect
import django.contrib
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import *
from .utils import *


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
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        color = request.POST.get('color')
        categoria = request.POST.get('categoria')
        imagenes = request.FILES.getlist('imagenes')
        try:
            # se valida la cantidad de imagenes
            if len(imagenes) > 5:
                raise Exception("No se pueden agregar más de 5 imágenes")
            formatos_permitidos = ['image/png', 'image/jpg', 'image/jpeg', "image/webp"]
            for imagen in imagenes:
                if imagen.content_type not in formatos_permitidos:
                    raise ValidationError(f"Formato no permitido: {imagen.content_type}. Solo se aceptan JPEG, PNG, GIF o WEBP.")
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                color=color,
                categoria=categoria
            )
            producto.save()
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)
            messages.success(request, 'Producto agregado correctamente')
        except ValidationError as ve:
            messages.error(request, f"Error de validacion: {ve}" )
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('administrador')
    else:
        return render(request, 'admin/productos/agregar_producto.html')

@session_rol_permission(1)
def editar_producto(request, id_producto):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        color = request.POST.get('color')
        categoria = request.POST.get('categoria')
        imagenes = request.FILES.getlist('imagenes')
        try:
            q = Producto.objects.get(id=id_producto)
            q.nombre = nombre
            q.descripcion = descripcion
            q.precio = precio
            q.stock = stock
            q.color = color
            q.categoria = categoria
            q.save()
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=q, imagen=imagen)
            messages.success(request, 'Producto editado correctamente')
        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('listar_productos')
    else:
        q = Producto.objects.get(id=id_producto)
        return render(request, 'admin/productos/editar_producto.html', {'producto': q})

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
    return render(request, 'admin/productos/detalle_producto.html', {'producto': producto})
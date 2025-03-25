from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'contrasena', 'rol')
    list_filter = ('rol',)
    search_fields = ('nombre', 'correo')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'color', 'en_oferta', 'precio_original', 'descuento')
    list_filter = ('categoria', 'color')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre', 'precio')

@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('id','producto', 'imagen')
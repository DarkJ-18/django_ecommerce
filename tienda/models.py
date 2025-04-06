from django.db import models
from decimal import Decimal

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=50)
    ROLES= (
        (1, "Administrador"),
        (2, "Cliente"),         
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=254)
    stock = models.IntegerField()
    color = models.CharField(max_length=20)
    CATEGORIAS = (
        (0, ""),
        (1, "Electrónica y Tecnología"),
        (2, "Moda y Accesorios"),
        (3, "Hogar y Muebles"),
        (4, "Salud y Belleza"),
        (5, "Deportes y Aire Libre"),
        (6, "Bebés y Niños"),
        (7, "Alimentos y Bebidas"),
        (8, "Libros, Música y Entretenimiento"),
        (9, "Mascotas"),
        (10, "Automotriz y Motocicletas")
    )
    categoria = models.IntegerField(choices=CATEGORIAS, default=0, null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def precio(self):
        """Calcula el precio final basado en el descuento."""
        if self.en_oferta and self.descuento > 0:
            return round(self.precio_original - (self.precio_original * self.descuento / Decimal(100)), 2)
        return self.precio_original

    def __str__(self):
        return f"{self.nombre} - ({self.stock} unidades)"
    
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
    



class Carrito(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True, related_name='carritos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def total(self):
        """Calcula el total del carrito sumando los subtotales de los elementos."""
        return sum(item.subtotal() for item in self.elementos.all()) # suma de los subtotales de cada elemento

    def __str__(self):
        return f"Carrito de {self.usuario.nombre if self.usuario else 'Invitado'}"

class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """Calcula el subtotal del elemento (precio del producto * cantidad)."""
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"
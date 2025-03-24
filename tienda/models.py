from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=50)
    ROLES= (
        (1, "Administrador"),
    )
    rol = models.IntegerField(choices=ROLES, default=1)
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
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
    
    def __str__(self):
        return f"{self.nombre} - {self.precio} - ({self.stock} unidades)"
    
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
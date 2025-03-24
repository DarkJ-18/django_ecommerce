from .models import *

def categorias(request):
    categorias = Producto.CATEGORIAS
    return {'categorias': categorias}
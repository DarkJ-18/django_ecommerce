from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .import views

# app_name = 'tienda' # para usar la url de la app en los templates

urlpatterns = [
    
    # vistas admin
    path('login/admin/', views.login, name='login'),
    path('logout/admin/', views.logout, name='logout'),
    path('administrador/', views.administrador, name='administrador'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
    
    # vistas del sitio
    path('', views.index, name='index'),
    path('detalle_producto/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('productos/categoria/<int:categoria>/', views.productos_por_categoria, name='productos_por_categoria'),
        # vistas de carrito
        path('carrito/', views.carrito, name='carrito'),
        path('carrito/agregar/<int:id_producto>/', views.agregar_carrito, name='agregar_carrito'),
        path('carrito/eliminar/<int:id_elemento>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
        path('carrito/actualizar/<int:id_elemento>/', views.actualizar_carrito, name='actualizar_carrito'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

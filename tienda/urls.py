from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .import views

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

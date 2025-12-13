from django.urls import path
from . import views

urlpatterns = [
     path('', views.login_view, name='login'),
     path('login/', views.login_view, name='login'),
     path('registro/', views.registro_view, name='registro'),
     path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nueva-venta/', views.nueva_venta, name='nueva_venta'),
    # path('venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    # path('historial/', views.historial_ventas, name='historial'),
    # path('productos/', views.productos, name='productos'),
    # path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]
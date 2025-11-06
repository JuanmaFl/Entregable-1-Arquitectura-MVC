from django.urls import path
from . import views
from .views import chatbot_api

# David Hernandez & Juan Manuel Florez

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('chatbot/', chatbot_api, name='chatbot_api'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    
    # Catálogo y carrito
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar-carrito/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    
    # Simulador de Red
    path('simulador/', views.simulador_red, name='simulador_red'),
    path('simulador/resultado/<int:simulacion_id>/', views.resultado_simulacion, name='resultado_simulacion'),
    path('mis-simulaciones/', views.mis_simulaciones, name='mis_simulaciones'),
    
    # API endpoints
    path('api/productos/', views.api_productos_json, name='api_productos_json'),
    path('api/clima/', views.obtener_clima, name='api_clima'),
    
    # Reportes con inversión de dependencias
    path('reportes/pdf/', views.generar_reporte_pdf, name='reporte_pdf'),
    path('reportes/excel/', views.generar_reporte_excel, name='reporte_excel'),
]
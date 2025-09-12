from django.urls import path
from . import views
from .views import chatbot_api


#David Hernandez

urlpatterns = [
    path('', views.home, name='home'),
    
    path('chatbot/', chatbot_api, name='chatbot_api'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar-carrito/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
]

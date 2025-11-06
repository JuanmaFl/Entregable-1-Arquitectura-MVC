from django.contrib import admin

# Register your models here.
from .models import Producto, ImagenProducto

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1  # cuántos campos vacíos aparecen por defecto

class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]
    list_display = ['nombre', 'precio']

admin.site.register(Producto, ProductoAdmin)
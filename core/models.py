from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# David Hernandez

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


# Juan Manuel Florez - Simulador de Red
class SimulacionRed(models.Model):
    # Usuario que realiza la simulación (opcional)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Datos de entrada del cliente
    latencia_actual = models.FloatField(help_text="Latencia actual en ms")
    perdida_paquetes_actual = models.FloatField(help_text="Pérdida de paquetes actual en %")
    ancho_banda_actual = models.FloatField(help_text="Ancho de banda actual en Mbps")
    trafico_pico = models.FloatField(help_text="Tráfico en hora pico en Gbps")
    num_usuarios = models.IntegerField(help_text="Número de usuarios concurrentes")
    
    # Servicios seleccionados
    servicio_pmaas = models.BooleanField(default=False, verbose_name="PMaaS")
    servicio_cdn = models.BooleanField(default=False, verbose_name="CDN IPTV")
    servicio_ddos = models.BooleanField(default=False, verbose_name="Anti DDoS")
    servicio_analisis = models.BooleanField(default=False, verbose_name="Análisis de Tráfico")
    
    # Resultados calculados por IA
    latencia_mejorada = models.FloatField(null=True, blank=True)
    perdida_paquetes_mejorada = models.FloatField(null=True, blank=True)
    ancho_banda_mejorado = models.FloatField(null=True, blank=True)
    mejora_porcentual = models.FloatField(null=True, blank=True)
    
    # Análisis y recomendaciones de IA
    analisis_ia = models.TextField(null=True, blank=True)
    recomendaciones_ia = models.TextField(null=True, blank=True)
    costo_estimado_mensual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roi_estimado_meses = models.IntegerField(null=True, blank=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ip_cliente = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Simulación de Red"
        verbose_name_plural = "Simulaciones de Red"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        usuario_nombre = self.usuario.email if self.usuario else "Anónimo"
        return f"Simulación {self.id} - {usuario_nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    @property
    def servicios_seleccionados(self):
        """Retorna lista de servicios seleccionados"""
        servicios = []
        if self.servicio_pmaas:
            servicios.append("PMaaS")
        if self.servicio_cdn:
            servicios.append("CDN IPTV")
        if self.servicio_ddos:
            servicios.append("Anti DDoS")
        if self.servicio_analisis:
            servicios.append("Análisis de Tráfico")
        return servicios
    
    @property
    def mejora_latencia_porcentaje(self):
        """Calcula mejora de latencia en porcentaje"""
        if self.latencia_mejorada and self.latencia_actual > 0:
            return ((self.latencia_actual - self.latencia_mejorada) / self.latencia_actual) * 100
        return 0
    
    @property
    def mejora_perdida_paquetes_porcentaje(self):
        """Calcula mejora de pérdida de paquetes en porcentaje"""
        if self.perdida_paquetes_mejorada is not None and self.perdida_paquetes_actual > 0:
            return ((self.perdida_paquetes_actual - self.perdida_paquetes_mejorada) / self.perdida_paquetes_actual) * 100
        return 0
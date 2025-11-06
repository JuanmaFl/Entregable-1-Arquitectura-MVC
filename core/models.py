from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name=_("Nombre"))
    descripcion = models.TextField(verbose_name=_("Descripción"))
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"))
    
    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")
    
    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes', verbose_name=_("Producto"))
    imagen = models.ImageField(upload_to='productos/', verbose_name=_("Imagen"))
    
    class Meta:
        verbose_name = _("Imagen de Producto")
        verbose_name_plural = _("Imágenes de Productos")
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class SimulacionRed(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Usuario"))
    
    latencia_actual = models.FloatField(verbose_name=_("Latencia actual (ms)"), help_text=_("Latencia actual en ms"))
    perdida_paquetes_actual = models.FloatField(verbose_name=_("Pérdida de paquetes actual (%)"), help_text=_("Pérdida de paquetes actual en %"))
    ancho_banda_actual = models.FloatField(verbose_name=_("Ancho de banda actual (Mbps)"), help_text=_("Ancho de banda actual en Mbps"))
    trafico_pico = models.FloatField(verbose_name=_("Tráfico en hora pico (Gbps)"), help_text=_("Tráfico en hora pico en Gbps"))
    num_usuarios = models.IntegerField(verbose_name=_("Número de usuarios"), help_text=_("Número de usuarios concurrentes"))
    
    servicio_pmaas = models.BooleanField(default=False, verbose_name=_("PMaaS"))
    servicio_cdn = models.BooleanField(default=False, verbose_name=_("CDN IPTV"))
    servicio_ddos = models.BooleanField(default=False, verbose_name=_("Anti DDoS"))
    servicio_analisis = models.BooleanField(default=False, verbose_name=_("Análisis de Tráfico"))
    
    latencia_mejorada = models.FloatField(null=True, blank=True, verbose_name=_("Latencia mejorada"))
    perdida_paquetes_mejorada = models.FloatField(null=True, blank=True, verbose_name=_("Pérdida de paquetes mejorada"))
    ancho_banda_mejorado = models.FloatField(null=True, blank=True, verbose_name=_("Ancho de banda mejorado"))
    mejora_porcentual = models.FloatField(null=True, blank=True, verbose_name=_("Mejora porcentual"))
    
    analisis_ia = models.TextField(null=True, blank=True, verbose_name=_("Análisis IA"))
    recomendaciones_ia = models.TextField(null=True, blank=True, verbose_name=_("Recomendaciones IA"))
    costo_estimado_mensual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Costo estimado mensual"))
    roi_estimado_meses = models.IntegerField(null=True, blank=True, verbose_name=_("ROI estimado (meses)"))
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    ip_cliente = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP del cliente"))
    
    class Meta:
        verbose_name = _("Simulación de Red")
        verbose_name_plural = _("Simulaciones de Red")
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        usuario_nombre = self.usuario.email if self.usuario else _("Anónimo")
        return f"{_('Simulación')} {self.id} - {usuario_nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    @property
    def servicios_seleccionados(self):
        servicios = []
        if self.servicio_pmaas:
            servicios.append("PMaaS")
        if self.servicio_cdn:
            servicios.append("CDN IPTV")
        if self.servicio_ddos:
            servicios.append("Anti DDoS")
        if self.servicio_analisis:
            servicios.append(_("Análisis de Tráfico"))
        return servicios
    
    @property
    def mejora_latencia_porcentaje(self):
        if self.latencia_mejorada and self.latencia_actual > 0:
            return ((self.latencia_actual - self.latencia_mejorada) / self.latencia_actual) * 100
        return 0
    
    @property
    def mejora_perdida_paquetes_porcentaje(self):
        if self.perdida_paquetes_mejorada is not None and self.perdida_paquetes_actual > 0:
            return ((self.perdida_paquetes_actual - self.perdida_paquetes_mejorada) / self.perdida_paquetes_actual) * 100
        return 0
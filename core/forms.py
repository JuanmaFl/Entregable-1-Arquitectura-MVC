from django import forms
from django.utils.translation import gettext_lazy as _
from .models import SimulacionRed

class SimuladorRedForm(forms.ModelForm):
    """
    Formulario para el simulador de red
    """
    
    class Meta:
        model = SimulacionRed
        fields = [
            'latencia_actual',
            'perdida_paquetes_actual',
            'ancho_banda_actual',
            'trafico_pico',
            'num_usuarios',
            'servicio_pmaas',
            'servicio_cdn',
            'servicio_ddos',
            'servicio_analisis',
        ]
        
        labels = {
            'latencia_actual': _('Latencia Actual'),
            'perdida_paquetes_actual': _('Pérdida de Paquetes Actual'),
            'ancho_banda_actual': _('Ancho de Banda Actual'),
            'trafico_pico': _('Tráfico en Hora Pico'),
            'num_usuarios': _('Número de Usuarios Concurrentes'),
            'servicio_pmaas': _('PMaaS - Optimización de Tráfico'),
            'servicio_cdn': _('CDN IPTV y Streaming'),
            'servicio_ddos': _('Protección Anti DDoS'),
            'servicio_analisis': _('Análisis de Tráfico Avanzado'),
        }
        
        widgets = {
            'latencia_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 45',
                'min': '0',
                'step': '0.1',
            }),
            'perdida_paquetes_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2.5',
                'min': '0',
                'max': '100',
                'step': '0.1',
            }),
            'ancho_banda_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 100',
                'min': '0',
                'step': '1',
            }),
            'trafico_pico': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 5',
                'min': '0',
                'step': '0.1',
            }),
            'num_usuarios': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500',
                'min': '1',
            }),
            'servicio_pmaas': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'servicio_cdn': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'servicio_ddos': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'servicio_analisis': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        
        help_texts = {
            'latencia_actual': _('Tiempo de respuesta de tu red en milisegundos (ms)'),
            'perdida_paquetes_actual': _('Porcentaje de paquetes perdidos (%)'),
            'ancho_banda_actual': _('Velocidad de conexión en Megabits por segundo (Mbps)'),
            'trafico_pico': _('Tráfico máximo en horas punta (Gbps)'),
            'num_usuarios': _('Cantidad de usuarios conectados simultáneamente'),
        }
    
    def clean_latencia_actual(self):
        latencia = self.cleaned_data.get('latencia_actual')
        if latencia < 0:
            raise forms.ValidationError(_("La latencia no puede ser negativa"))
        if latencia > 1000:
            raise forms.ValidationError(_("La latencia parece excesivamente alta. Por favor verifica."))
        return latencia
    
    def clean_perdida_paquetes_actual(self):
        perdida = self.cleaned_data.get('perdida_paquetes_actual')
        if perdida < 0 or perdida > 100:
            raise forms.ValidationError(_("La pérdida de paquetes debe estar entre 0 y 100%"))
        return perdida
    
    def clean_ancho_banda_actual(self):
        ancho_banda = self.cleaned_data.get('ancho_banda_actual')
        if ancho_banda <= 0:
            raise forms.ValidationError(_("El ancho de banda debe ser mayor a 0"))
        return ancho_banda
    
    def clean_trafico_pico(self):
        trafico = self.cleaned_data.get('trafico_pico')
        if trafico < 0:
            raise forms.ValidationError(_("El tráfico no puede ser negativo"))
        return trafico
    
    def clean_num_usuarios(self):
        usuarios = self.cleaned_data.get('num_usuarios')
        if usuarios < 1:
            raise forms.ValidationError(_("Debe haber al menos 1 usuario"))
        if usuarios > 1000000:
            raise forms.ValidationError(_("El número de usuarios parece excesivo. Por favor verifica."))
        return usuarios
    
    def clean(self):
        cleaned_data = super().clean()
        
        servicios = [
            cleaned_data.get('servicio_pmaas'),
            cleaned_data.get('servicio_cdn'),
            cleaned_data.get('servicio_ddos'),
            cleaned_data.get('servicio_analisis'),
        ]
        
        if not any(servicios):
            raise forms.ValidationError(
                _("Debes seleccionar al menos un servicio para simular.")
            )
        
        return cleaned_data
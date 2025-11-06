import openai
from django.conf import settings
import json

# Juan Manuel Florez

openai.api_key = settings.OPENAI_API_KEY


class SimuladorCalculator:
    """
    Clase para calcular mejoras en la red basado en servicios seleccionados
    """
    
    # Factores de mejora por servicio
    MEJORAS_LATENCIA = {
        'pmaas': 0.25,      # 25% de mejora
        'cdn': 0.40,        # 40% de mejora
        'ddos': 0.10,       # 10% de mejora
        'analisis': 0.15,   # 15% de mejora
    }
    
    MEJORAS_PERDIDA_PAQUETES = {
        'pmaas': 0.30,
        'cdn': 0.25,
        'ddos': 0.45,
        'analisis': 0.20,
    }
    
    MEJORAS_ANCHO_BANDA = {
        'pmaas': 0.20,
        'cdn': 0.35,
        'ddos': 0.05,
        'analisis': 0.10,
    }
    
    # Costos base mensuales por servicio (USD)
    COSTOS_SERVICIO = {
        'pmaas': 500,
        'cdn': 800,
        'ddos': 600,
        'analisis': 400,
    }
    
    @staticmethod
    def calcular_mejoras(simulacion):
        """
        Calcula las mejoras en la red basado en los servicios seleccionados
        """
        # Determinar servicios activos
        servicios_activos = []
        if simulacion.servicio_pmaas:
            servicios_activos.append('pmaas')
        if simulacion.servicio_cdn:
            servicios_activos.append('cdn')
        if simulacion.servicio_ddos:
            servicios_activos.append('ddos')
        if simulacion.servicio_analisis:
            servicios_activos.append('analisis')
        
        # Calcular mejoras acumulativas
        mejora_latencia_total = sum(
            SimuladorCalculator.MEJORAS_LATENCIA.get(s, 0) 
            for s in servicios_activos
        )
        mejora_perdida_total = sum(
            SimuladorCalculator.MEJORAS_PERDIDA_PAQUETES.get(s, 0) 
            for s in servicios_activos
        )
        mejora_ancho_banda_total = sum(
            SimuladorCalculator.MEJORAS_ANCHO_BANDA.get(s, 0) 
            for s in servicios_activos
        )
        
        # Limitar mejoras al 90% máximo (realista)
        mejora_latencia_total = min(mejora_latencia_total, 0.90)
        mejora_perdida_total = min(mejora_perdida_total, 0.95)
        mejora_ancho_banda_total = min(mejora_ancho_banda_total, 0.80)
        
        # Aplicar mejoras
        simulacion.latencia_mejorada = simulacion.latencia_actual * (1 - mejora_latencia_total)
        simulacion.perdida_paquetes_mejorada = simulacion.perdida_paquetes_actual * (1 - mejora_perdida_total)
        simulacion.ancho_banda_mejorado = simulacion.ancho_banda_actual * (1 + mejora_ancho_banda_total)
        
        # Calcular mejora porcentual promedio
        simulacion.mejora_porcentual = (
            (mejora_latencia_total + mejora_perdida_total + mejora_ancho_banda_total) / 3
        ) * 100
        
        # Calcular costo mensual
        simulacion.costo_estimado_mensual = sum(
            SimuladorCalculator.COSTOS_SERVICIO.get(s, 0) 
            for s in servicios_activos
        )
        
        # Calcular ROI estimado (simplificado)
        # Asumiendo ahorro de 30% en costos operativos por mejoras
        ahorro_mensual_estimado = simulacion.costo_estimado_mensual * 2  # El ahorro es mayor que la inversión
        simulacion.roi_estimado_meses = max(
            int(simulacion.costo_estimado_mensual / ahorro_mensual_estimado * 12), 
            3
        )
        
        return simulacion


class AnalizadorIA:
    """
    Clase para generar análisis y recomendaciones usando OpenAI
    """
    
    @staticmethod
    def generar_analisis(simulacion):
        """
        Genera un análisis detallado usando GPT-4
        """
        # Preparar contexto para la IA
        servicios_nombres = {
            'pmaas': 'PMaaS (Optimización de Tráfico)',
            'cdn': 'CDN IPTV y Streaming',
            'ddos': 'Protección Anti DDoS',
            'analisis': 'Análisis de Tráfico Avanzado'
        }
        
        servicios_seleccionados = []
        if simulacion.servicio_pmaas:
            servicios_seleccionados.append(servicios_nombres['pmaas'])
        if simulacion.servicio_cdn:
            servicios_seleccionados.append(servicios_nombres['cdn'])
        if simulacion.servicio_ddos:
            servicios_seleccionados.append(servicios_nombres['ddos'])
        if simulacion.servicio_analisis:
            servicios_seleccionados.append(servicios_nombres['analisis'])
        
        prompt = f"""
Eres un experto en redes y telecomunicaciones de Peering Latam. 
Analiza los siguientes datos de red de un cliente y proporciona un análisis profesional y detallado:

DATOS ACTUALES DEL CLIENTE:
- Latencia: {simulacion.latencia_actual} ms
- Pérdida de paquetes: {simulacion.perdida_paquetes_actual}%
- Ancho de banda: {simulacion.ancho_banda_actual} Mbps
- Tráfico en hora pico: {simulacion.trafico_pico} Gbps
- Usuarios concurrentes: {simulacion.num_usuarios}

SERVICIOS SELECCIONADOS:
{', '.join(servicios_seleccionados)}

RESULTADOS PROYECTADOS:
- Latencia mejorada: {simulacion.latencia_mejorada:.2f} ms (mejora de {simulacion.mejora_latencia_porcentaje:.1f}%)
- Pérdida de paquetes mejorada: {simulacion.perdida_paquetes_mejorada:.2f}% (mejora de {simulacion.mejora_perdida_paquetes_porcentaje:.1f}%)
- Ancho de banda mejorado: {simulacion.ancho_banda_mejorado:.2f} Mbps
- Inversión mensual estimada: ${simulacion.costo_estimado_mensual} USD

Por favor proporciona:
1. Un análisis técnico de la situación actual (2-3 párrafos)
2. Explicación de cómo los servicios seleccionados mejorarán específicamente su red
3. Beneficios concretos que experimentará el cliente
4. Métricas clave de rendimiento esperadas

Sé específico, técnico pero comprensible, y persuasivo. Usa un tono profesional.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un consultor experto en redes y telecomunicaciones de Peering Latam. Proporciona análisis técnicos detallados, precisos y persuasivos."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            
            analisis = response.choices[0].message.content
            return analisis
            
        except Exception as e:
            # Fallback si falla la IA
            return AnalizadorIA._generar_analisis_fallback(simulacion)
    
    @staticmethod
    def generar_recomendaciones(simulacion):
        """
        Genera recomendaciones personalizadas usando GPT-4
        """
        prompt = f"""
Basándote en estos datos de red:
- Latencia actual: {simulacion.latencia_actual} ms
- Pérdida de paquetes: {simulacion.perdida_paquetes_actual}%
- {simulacion.num_usuarios} usuarios concurrentes

Proporciona 4-5 recomendaciones específicas y accionables para optimizar su red con nuestros servicios.
Cada recomendación debe ser:
- Concreta y específica
- Técnicamente sólida
- Orientada a resultados
- Breve (1-2 oraciones)

Formato: Lista numerada.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un consultor de redes especializado en dar recomendaciones prácticas y accionables."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )
            
            recomendaciones = response.choices[0].message.content
            return recomendaciones
            
        except Exception as e:
            return AnalizadorIA._generar_recomendaciones_fallback(simulacion)
    
    @staticmethod
    def _generar_analisis_fallback(simulacion):
        """Análisis de respaldo si falla la IA"""
        return f"""
**Análisis de Tu Red Actual**

Tu red presenta una latencia de {simulacion.latencia_actual} ms y una pérdida de paquetes del {simulacion.perdida_paquetes_actual}%, con {simulacion.num_usuarios} usuarios concurrentes. Estos valores indican oportunidades significativas de mejora.

**Impacto de Nuestros Servicios**

Con los servicios seleccionados de Peering Latam, proyectamos una reducción de latencia hasta {simulacion.latencia_mejorada:.2f} ms (mejora del {simulacion.mejora_latencia_porcentaje:.1f}%) y una disminución en la pérdida de paquetes a {simulacion.perdida_paquetes_mejorada:.2f}%. 

**Beneficios Esperados**

Tu red experimentará mayor estabilidad, mejor experiencia de usuario en aplicaciones de tiempo real, y optimización del uso de recursos de red. La inversión estimada de ${simulacion.costo_estimado_mensual} USD mensuales se traducirá en ahorros operativos y mayor satisfacción del usuario final.
"""
    
    @staticmethod
    def _generar_recomendaciones_fallback(simulacion):
        """Recomendaciones de respaldo si falla la IA"""
        return """
1. Implementar monitoreo continuo de latencia y pérdida de paquetes para identificar cuellos de botella
2. Optimizar rutas de tráfico mediante peering directo con proveedores de contenido
3. Configurar balanceo de carga para distribuir tráfico en horas pico
4. Implementar cache local para contenido frecuentemente accedido
5. Establecer políticas de QoS para priorizar tráfico crítico
"""
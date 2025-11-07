from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages
import openai, dateparser
import json
import requests
from datetime import datetime, date

from .models import Producto, SimulacionRed
from .forms import SimuladorRedForm
from .simulador_utils import SimuladorCalculator, AnalizadorIA
from .services.report_generator import PDFReportGenerator, ExcelReportGenerator, ReportService

# Asigna la API key desde settings
openai.api_key = settings.OPENAI_API_KEY


# Juan Manuel Florez

from django.utils.translation import gettext_lazy as _

def home(request):
    horas = [f"{h:02d}:00" for h in range(8, 20)]
    clientes = [
        {'nombre': 'Tigo', 'descripcion': _('Proveedor regional de telecomunicaciones.'), 'logo': 'core/img/clientes/tigo.png'},
        {'nombre': 'Ufinet', 'descripcion': _('Operador mayorista de fibra óptica.'), 'logo': 'core/img/clientes/ufinet.jpg'},
        {'nombre': 'Mundo Pacífico', 'descripcion': _('Proveedor de internet y TV en Chile.'), 'logo': 'core/img/clientes/mundo.jpg'},
        {'nombre': 'Colombia Más', 'descripcion': _('Red nacional para servicios residenciales.'), 'logo': 'core/img/clientes/colombiamas.jpg'},
    ]
    productos = [
        {
            'nombre': 'Flow',
            'descripcion': _('Visualización de tráfico con mapas de calor y flujos de red para detectar cuellos de botella.'),
            'imagen': 'core/img/productos/flow.png'
        },
        {
            'nombre': 'Grafana',
            'descripcion': _('Dashboard para monitorear servicios, tráfico, métricas y alarmas desde diversas fuentes.'),
            'imagen': 'core/img/productos/grafana.png'
        },
        {
            'nombre': 'MOTTS',
            'descripcion': _('Monitoreo de tráfico OTT especializado en gaming, streaming y contenido sensible.'),
            'imagen': 'core/img/productos/motts.png'
        },
    ]
    return render(request, "core/home.html", {
        "horas": horas,
        "today": date.today().isoformat(),
        "productos": productos,
        "clientes": clientes
    })


@csrf_exempt
@login_required
def chatbot_api(request):
    if request.method != 'POST':
        return JsonResponse({'reply': 'Método no permitido'}, status=405)

    data = json.loads(request.body)
    user_message = data.get('message', '').strip()

    # Conversación únicamente para asistencia técnica o preguntas frecuentes
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "Eres un asistente virtual en el sitio web de Peering Latam. "
                "Respondes preguntas técnicas, dudas frecuentes sobre servicios, productos, procesos, "
                "información institucional, y soporte general. "
                "Evita agendar citas o recoger datos personales. "
                "Habla con un tono profesional, claro y cercano. "
                "Carlos Florez es el fundador de la empresa, menciónalo si preguntan por el fundador. "
                "Intenta motivar a las personas de forma persuasiva a comprar nuestros servicios."
            )},
            {"role": "user", "content": user_message}
        ]
    )
    reply = gpt_response.choices[0].message.content

    return JsonResponse({'reply': reply})


@login_required
def agendar_cita(request):
    cita_confirmada = False
    horas = [f"{h:02d}:00" for h in range(8, 20)]

    if request.method == "POST":
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        asunto = request.POST.get("asunto")

        if fecha and hora and asunto:
            subject = "Nueva cita agendada"
            from_email = settings.EMAIL_HOST_USER
            to_email = [request.user.email, settings.EMAIL_HOST_USER]

            context = {
                "usuario": request.user,
                "fecha": fecha,
                "hora": hora,
                "asunto": asunto,
            }

            text_content = f"Cita para el {fecha} a las {hora}.\nAsunto: {asunto}"
            html_content = render_to_string("emails/cita_confirmada.html", context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()

            cita_confirmada = True

    return render(request, "core/home.html", {
        "cita_confirmada": cita_confirmada,
        "today": date.today().isoformat(),
        "horas": horas
    })


def catalogo_view(request):
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 6)

    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render(request, 'core/catalogo.html', {'productos': productos})


def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def eliminar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        productos.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'core/carrito.html', {'productos': productos, 'total': total})


# ============================================
# SIMULADOR DE RED
# ============================================
@login_required
def simulador_red(request):
    """
    Vista principal del simulador de red
    Permite a cualquier usuario simular mejoras en su red
    """
    if request.method == 'POST':
        form = SimuladorRedForm(request.POST)
        
        if form.is_valid():
            # Guardar datos base
            simulacion = form.save(commit=False)
            
            # Asociar usuario si está autenticado
            if request.user.is_authenticated:
                simulacion.usuario = request.user
            
            # Guardar IP del cliente
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                simulacion.ip_cliente = x_forwarded_for.split(',')[0]
            else:
                simulacion.ip_cliente = request.META.get('REMOTE_ADDR')
            
            # Calcular mejoras
            simulacion = SimuladorCalculator.calcular_mejoras(simulacion)
            
            # Generar análisis con IA
            try:
                simulacion.analisis_ia = AnalizadorIA.generar_analisis(simulacion)
                simulacion.recomendaciones_ia = AnalizadorIA.generar_recomendaciones(simulacion)
            except Exception as e:
                print(f"Error al generar análisis IA: {e}")
                # Los fallbacks se aplicarán automáticamente
            
            # Guardar simulación completa
            simulacion.save()
            
            # Redirigir a resultados
            return redirect('resultado_simulacion', simulacion_id=simulacion.id)
    else:
        form = SimuladorRedForm()
    
    context = {
        'form': form,
        'title': 'Simulador de Red Inteligente',
    }
    
    return render(request, 'core/simulador.html', context)

from django.utils.translation import get_language

@login_required


def resultado_simulacion(request, simulacion_id):
    """
    Muestra los resultados de una simulación
    """
    simulacion = get_object_or_404(SimulacionRed, id=simulacion_id)
    
    # Detectar idioma actual
    idioma = get_language()
    
    # Regenerar análisis si no existe o si cambió el idioma
    if not simulacion.analisis_ia or request.GET.get('regenerar'):
        try:
            simulacion.analisis_ia = AnalizadorIA.generar_analisis(simulacion, idioma)
            simulacion.recomendaciones_ia = AnalizadorIA.generar_recomendaciones(simulacion, idioma)
            simulacion.save()
        except Exception as e:
            print(f"Error al generar análisis IA: {e}")
    
    # Preparar datos para gráficos
    datos_grafico = {
        'labels': ['Latencia (ms)', 'Pérdida Paquetes (%)', 'Ancho de Banda (Mbps)'],
        'antes': [
            float(simulacion.latencia_actual),
            float(simulacion.perdida_paquetes_actual),
            float(simulacion.ancho_banda_actual)
        ],
        'despues': [
            float(simulacion.latencia_mejorada),
            float(simulacion.perdida_paquetes_mejorada),
            float(simulacion.ancho_banda_mejorado)
        ]
    }
    
    context = {
        'simulacion': simulacion,
        'datos_grafico': json.dumps(datos_grafico),
        'mejora_latencia': simulacion.mejora_latencia_porcentaje,
        'mejora_perdida': simulacion.mejora_perdida_paquetes_porcentaje,
    }
    
    return render(request, 'core/resultado_simulacion.html', context)

@login_required
def mis_simulaciones(request):
    """
    Lista todas las simulaciones del usuario autenticado
    """
    simulaciones = SimulacionRed.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    context = {
        'simulaciones': simulaciones,
    }
    
    return render(request, 'core/mis_simulaciones.html', context)


# ============================================
# API Y SERVICIOS WEB
# ============================================

def api_productos_json(request):
    """
    Servicio web que provee información de productos en formato JSON
    """
    productos = Producto.objects.all()
    productos_data = []

    for producto in productos:
        producto_info = {
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'url': request.build_absolute_uri(f'/catalogo/'),
            'detalle_url': request.build_absolute_uri(f'/catalogo/'),
        }

        imagenes = producto.imagenes.all()
        if imagenes:
            producto_info['imagenes'] = [
                request.build_absolute_uri(img.imagen.url) for img in imagenes
            ]

        productos_data.append(producto_info)

    return JsonResponse({
        'status': 'success',
        'total_productos': len(productos_data),
        'productos': productos_data,
        'proveedor': 'Peering Latam',
        'timestamp': datetime.now().isoformat()
    }, safe=False)


def obtener_clima(request):
    """
    Consume API externa de clima
    """
    try:
        ciudad = 'Medellin'
        response = requests.get(f'https://wttr.in/{ciudad}?format=j1', timeout=5)

        if response.status_code == 200:
            data = response.json()
            clima = {
                'temperatura': data['current_condition'][0]['temp_C'],
                'descripcion': data['current_condition'][0]['weatherDesc'][0]['value'],
                'humedad': data['current_condition'][0]['humidity'],
                'ciudad': ciudad
            }
            return JsonResponse(clima)
        else:
            return JsonResponse({'error': 'No se pudo obtener el clima'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def generar_reporte_pdf(request):
    """
    Genera un reporte de productos en formato PDF
    """
    productos = Producto.objects.all()
    report_service = ReportService(PDFReportGenerator())
    return report_service.create_report(productos, "reporte_productos.pdf")


@login_required
def generar_reporte_excel(request):
    """
    Genera un reporte de productos en formato Excel (CSV)
    """
    productos = Producto.objects.all()
    report_service = ReportService(ExcelReportGenerator())
    return report_service.create_report(productos, "reporte_productos.csv")


from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import openai, dateparser
import json
from datetime import datetime
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Producto

# Asigna la API key desde settings
openai.api_key = settings.OPENAI_API_KEY






def home(request):
    horas = [f"{h:02d}:00" for h in range(8, 20)]
    clientes = [
        {'nombre': 'Tigo', 'descripcion': 'Proveedor regional de telecomunicaciones.', 'logo': 'core/img/clientes/tigo.png'},
        {'nombre': 'Ufinet', 'descripcion': 'Operador mayorista de fibra óptica.', 'logo': 'core/img/clientes/ufinet.jpg'},
        {'nombre': 'Mundo Pacífico', 'descripcion': 'Proveedor de internet y TV en Chile.', 'logo': 'core/img/clientes/mundo.jpg'},
        {'nombre': 'Colombia Más', 'descripcion': 'Red nacional para servicios residenciales.', 'logo': 'core/img/clientes/colombiamas.jpg'},
    ]
    productos = [
        {
            'nombre': 'Flow',
            'descripcion': 'Visualización de tráfico con mapas de calor y flujos de red para detectar cuellos de botella.',
            'imagen': 'core/img/productos/flow.png'
        },
        {
            'nombre': 'Grafana',
            'descripcion': 'Dashboard para monitorear servicios, tráfico, métricas y alarmas desde diversas fuentes.',
            'imagen': 'core/img/productos/grafana.png'
        },
        {
            'nombre': 'MOTTS',
            'descripcion': 'Monitoreo de tráfico OTT especializado en gaming, streaming y contenido sensible.',
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
    cita_confirmada = False  # Estado inicial
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
        "horas": [f"{h:02d}:00" for h in range(8, 20)]
    })


def catalogo_view(request):
    productos = Producto.objects.all()
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

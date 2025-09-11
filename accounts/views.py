from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Mensaje en texto plano (fallback)
            text_message = f"""
Hola {user.full_name},

Gracias por registrarte en Peering Latam.

Somos expertos en conectividad, optimización de tráfico de red y soluciones en telecomunicaciones.

Tu cuenta ya está activa. Accede a nuestros servicios iniciando sesión.

Saludos,
Equipo Peering Latam
https://www.peeringlatam.com.br
"""

            # Mensaje HTML
            html_message = f"""
                <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto; border:1px solid #eee; padding:20px;">
                    <h2 style="color:#00AEEF;">¡Bienvenido a Peering Latam!</h2>
                    <p>Hola <strong>{user.full_name}</strong>,</p>
                    <p>Gracias por registrarte en nuestra plataforma. Ya puedes acceder a nuestras soluciones en telecomunicaciones, nube, infraestructura y seguridad corporativa.</p>
                    <p>🔗 <a href="https://www.peeringlatam.com.br" style="color:#00AEEF;">Visítanos</a> para conocer más.</p>
                    <hr>
                    <p style="font-size:0.85rem; color:#777;">Este correo fue generado automáticamente. Si tienes dudas, escríbenos a soporte@peeringlatam.com.br.</p>
                </div>
            """

            send_mail(
                subject='Bienvenido a Peering Latam 🚀',
                message=text_message,
                from_email='Peering Latam <noreply@peeringlatam.com>',
                recipient_list=[user.email],
                fail_silently=False,
                html_message=html_message,
            )

            messages.success(request, "Cuenta creada exitosamente. ¡Revisa tu correo!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

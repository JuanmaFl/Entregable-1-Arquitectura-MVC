"""
URL configuration for peeringlatam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Desarrollado por: David Hernandez, Juan Manuel Florez, Carlos Florez Mesa

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# ============================================
# URLs SIN PATRÓN DE IDIOMA
# (No requieren prefijo de idioma como /es/ o /en/)
# ============================================
urlpatterns = [
    # URL para cambiar el idioma - CRÍTICO para que funcione el selector
    path('i18n/', include('django.conf.urls.i18n')),
]

# ============================================
# URLs CON PATRÓN DE IDIOMA
# (Estas URLs tendrán prefijo /es/ o /en/ según el idioma seleccionado)
# ============================================
urlpatterns += i18n_patterns(
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # URLs de la app principal (core)
    path('', include('core.urls')),
    
    # URLs de la app de cuentas (accounts)
    path('accounts/', include('accounts.urls')),
    
    # Prefijo de idioma para estas rutas
    prefix_default_language=True,  # ✅ OPCIONAL: Si quieres que /es/ aparezca en español también
)

# ============================================
# ARCHIVOS MEDIA (solo en desarrollo)
# ============================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ============================================
# CONFIGURACIÓN DE ADMIN (OPCIONAL - Personalización)
# ============================================
admin.site.site_header = "Peering Latam - Administración"
admin.site.site_title = "Peering Latam Admin"
admin.site.index_title = "Panel de Control"



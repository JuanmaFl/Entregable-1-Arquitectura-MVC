# Peering Latam - Plataforma Web Django

Proyecto academico desarrollado en Django que implementa arquitectura MVC con servicios y Docker.

## Caracteristicas Implementadas - Entregable 2

### Funcionalidades Principales
- Catalogo de productos con carrito de compras
- Sistema de autenticacion de usuarios personalizado
- Chatbot asistente virtual integrado con OpenAI
- Agendamiento de citas con confirmacion por correo electronico
- Sistema de internacionalizacion (Espanol e Ingles)
- Servicio web JSON para compartir informacion de productos
- Consumo de API externa de clima
- Inversion de dependencias para generacion de reportes (PDF y Excel)
- Sistema de paginacion en catalogo
- Animaciones con anime.js
- Breadcrumbs navigation en todas las vistas
- Diseno responsive para movil y escritorio

### Arquitectura y Patrones
- Arquitectura MVC (Model-View-Controller)
- Inversion de dependencias para reportes
- Servicios web RESTful
- Pruebas unitarias

### Usabilidad
- Estructura visual consistente en todas las vistas
- Formularios bien disenados que mantienen datos al encontrar errores
- Sistema de navegacion con breadcrumbs
- Diseno responsive
- Animaciones suaves con anime.js
- Widget de clima en tiempo real

## Requisitos

- Python 3.10 o superior
- pip
- Docker y docker-compose (para despliegue)
- Cuenta de OpenAI API (para chatbot)
- Configuracion de email SMTP (para notificaciones)

## Instalacion y Ejecucion

### Opcion 1: Ejecucion Local

1. Clonar el repositorio

```bash
git clone https://github.com/JuanmaFl/Entregable-1-Arquitectura-MVC.git
cd Entregable-1-Arquitectura-MVC
```

2. Crear y activar entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno

Copiar .env.example a .env y configurar:

```bash
cp .env.example .env
```

Editar .env con tus credenciales:
- OPENAI_API_KEY
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

5. Aplicar migraciones

```bash
python manage.py migrate
```

6. Crear superusuario

```bash
python manage.py createsuperuser
```

7. Ejecutar el servidor

```bash
python manage.py runserver
```

### Opcion 2: Despliegue con Docker

1. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

2. Construir y ejecutar con docker-compose

```bash
docker-compose up --build
```

La aplicacion estara disponible en http://localhost:80

## Endpoints de API

### Servicio Web JSON
- GET /api/productos/ - Lista de productos en formato JSON

### API Externa
- GET /api/clima/ - Informacion del clima en tiempo real

### Reportes
- GET /reportes/pdf/ - Generar reporte de productos en PDF
- GET /reportes/excel/ - Generar reporte de productos en Excel (CSV)

## Pruebas Unitarias

Ejecutar pruebas:

```bash
python manage.py test
```

Las pruebas cubren:
- Modelo de productos
- API de productos JSON

## Estructura del Proyecto

```
Entregable-1-Arquitectura-MVC/
├── accounts/              # App de autenticacion
├── core/                  # App principal
│   ├── services/         # Servicios (inversion de dependencias)
│   ├── static/           # Archivos estaticos
│   └── templates/        # Templates HTML
├── peeringlatam/         # Configuracion del proyecto
├── templates/            # Templates base
├── media/                # Archivos multimedia
├── Dockerfile            # Configuracion Docker
├── docker-compose.yml    # Orquestacion de servicios
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

## Tecnologias Utilizadas

- Django 5.1.6
- Python 3.10
- OpenAI API
- PostgreSQL (produccion)
- SQLite (desarrollo)
- Docker
- Nginx
- Gunicorn
- Bootstrap 5
- Anime.js
- AOS (Animate On Scroll)

## Autores

- Juan Manuel Florez
- David Hernandez
- Carlos Florez Mesa

## Licencia

Proyecto academico - Topicos Especiales en Ingenieria de Software

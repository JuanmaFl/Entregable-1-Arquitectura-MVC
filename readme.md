# 🌐 Peering Latam – Plataforma Web (Django)

Este es un proyecto académico desarrollado en **Django** que implementa:

- ✅ Catálogo de productos y carrito de compras.
- ✅ Chatbot asistente virtual integrado con OpenAI para soporte y preguntas frecuentes.
- ✅ Agendamiento de citas con confirmación por correo electrónico.
- ✅ Despliegue de la información del usuario autenticado en la interfaz.

Es parte de una actividad académica para demostrar funcionalidades web en Django.

---

## 🚀 Requisitos

- Python 3.10 o superior  
- pip  
- Entorno virtual (recomendado)  
- Base de datos (SQLite por defecto o la que configures en `settings.py`)  
- Configuración de claves API (por ejemplo `OPENAI_API_KEY` en tu `.env` o `settings.py`)

---

## 📥 Instalación y Ejecución

1. **Clonar este repositorio**

   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPO.git
   cd TU_REPO

2 **Crear un entorno virtual y activarlo**

bash
Copiar código
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

3 **Instalar dependencias**

bash
Copiar código
pip install -r requirements.txt


4 **Aplicar migraciones**

bash
Copiar código
python manage.py migrate

5 **Crear un superusuario (opcional)**

bash
Copiar código
python manage.py createsuperuser

6 **Ejecutar el servidor**

bash
Copiar código
python manage.py runserver
from django.test import TestCase, Client
from django.urls import reverse
from .models import Producto
from .services.report_generator import PDFReportGenerator, ExcelReportGenerator, ReportService


class ProductoModelTest(TestCase):
    """
    Prueba unitaria simple para el modelo Producto
    Verifica la creacion y representacion de productos
    """

    def setUp(self):
        """Crea un producto de prueba"""
        self.producto = Producto.objects.create(
            nombre="Router Cisco",
            descripcion="Router empresarial de alta velocidad",
            precio=1500.00
        )

    def test_producto_creation(self):
        """Prueba que el producto se crea correctamente"""
        self.assertEqual(self.producto.nombre, "Router Cisco")
        self.assertEqual(self.producto.descripcion, "Router empresarial de alta velocidad")
        self.assertEqual(self.producto.precio, 1500.00)

    def test_producto_str(self):
        """Prueba el metodo __str__ del producto"""
        self.assertEqual(str(self.producto), "Router Cisco")


class APIProductosTest(TestCase):
    """
    Prueba unitaria simple para el endpoint de API de productos
    Verifica que el servicio JSON funciona correctamente
    """

    def setUp(self):
        """Crea productos de prueba"""
        self.client = Client()
        Producto.objects.create(
            nombre="Switch Cisco",
            descripcion="Switch de 48 puertos",
            precio=800.00
        )
        Producto.objects.create(
            nombre="Firewall Fortinet",
            descripcion="Firewall empresarial",
            precio=2000.00
        )

    def test_api_productos_json(self):
        """Prueba que la API retorna JSON correctamente"""
        response = self.client.get(reverse('api_productos_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['total_productos'], 2)
        self.assertEqual(len(data['productos']), 2)

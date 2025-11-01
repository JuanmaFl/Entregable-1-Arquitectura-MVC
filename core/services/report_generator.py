"""
Inversion de Dependencias - Generacion de Reportes
Implementa una interfaz abstracta y dos clases concretas para generar reportes
"""

from abc import ABC, abstractmethod
from django.http import HttpResponse
from io import BytesIO
import csv


class ReportGenerator(ABC):
    """
    Interfaz abstracta para generadores de reportes
    Define el contrato que deben cumplir las clases concretas
    """

    @abstractmethod
    def generate_report(self, productos, filename):
        """
        Metodo abstracto para generar reportes
        Args:
            productos: Lista de productos a incluir en el reporte
            filename: Nombre del archivo a generar
        Returns:
            HttpResponse con el archivo generado
        """
        pass


class PDFReportGenerator(ReportGenerator):
    """
    Clase concreta para generar reportes en formato PDF
    """

    def generate_report(self, productos, filename="reporte_productos.pdf"):
        """
        Genera un reporte en formato PDF
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Titulo
            title = Paragraph("<b>Reporte de Productos - Peering Latam</b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 0.3 * inch))

            # Tabla de productos
            data = [['ID', 'Nombre', 'Descripcion', 'Precio']]
            for producto in productos:
                data.append([
                    str(producto.id),
                    producto.nombre,
                    producto.descripcion[:50] + '...' if len(producto.descripcion) > 50 else producto.descripcion,
                    f'${producto.precio}'
                ])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)

            doc.build(elements)
            buffer.seek(0)

            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except ImportError:
            # Si reportlab no esta instalado, retorna un mensaje de error
            response = HttpResponse("Error: reportlab no esta instalado. Instale con: pip install reportlab")
            response.status_code = 500
            return response


class ExcelReportGenerator(ReportGenerator):
    """
    Clase concreta para generar reportes en formato Excel (CSV)
    """

    def generate_report(self, productos, filename="reporte_productos.csv"):
        """
        Genera un reporte en formato CSV (compatible con Excel)
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nombre', 'Descripcion', 'Precio'])

        for producto in productos:
            writer.writerow([
                producto.id,
                producto.nombre,
                producto.descripcion,
                float(producto.precio)
            ])

        return response


class ReportService:
    """
    Servicio que utiliza la inversion de dependencias
    Permite cambiar entre diferentes generadores de reportes
    """

    def __init__(self, generator: ReportGenerator):
        """
        Constructor que recibe un generador de reportes
        Args:
            generator: Instancia de una clase que implemente ReportGenerator
        """
        self.generator = generator

    def create_report(self, productos, filename=None):
        """
        Crea un reporte usando el generador configurado
        """
        return self.generator.generate_report(productos, filename)

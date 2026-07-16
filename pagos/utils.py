import os
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

from reservas.models import Reserva

# ========== DATOS DE LA EMPRESA ==========
EMPRESA = {
    'nombre': getattr(settings, 'EMPRESA_NOMBRE', 'CanchaFácil'),
    'nit': getattr(settings, 'EMPRESA_NIT', '900.123.456-7'),
    'direccion': getattr(settings, 'EMPRESA_DIRECCION', 'Calle Falsa 123, Bogotá'),
    'telefono': getattr(settings, 'EMPRESA_TELEFONO', '+57 300 123 4567'),
    'correo': getattr(settings, 'EMPRESA_CORREO', 'info@canchafacil.com'),
    'logo': getattr(settings, 'EMPRESA_LOGO', 'img/logo-green.png'),  # Ruta relativa dentro de static
}

# ========== COLORES ==========
COLOR_VERDE_OSCURO = colors.HexColor('#62ff00')
COLOR_VERDE_CLARO = colors.HexColor('#E8F5E9')
COLOR_BLANCO = colors.white
COLOR_NEGRO = colors.black

# ========== PRECIO POR HORA ==========
PRECIO_POR_HORA = Decimal('50000')

# ========== FUNCIÓN PARA ENCONTRAR EL LOGO ==========
def encontrar_logo():
    """
    Busca el archivo del logo en varias ubicaciones.
    Retorna la ruta absoluta si existe, o None si no.
    """
    # Obtener la ruta relativa del logo desde la configuración
    logo_relativo = EMPRESA.get('logo', 'img/logo-green.png')
    
    # Lista de posibles ubicaciones donde buscar
    posibles_ubicaciones = []
    
    # 1. STATIC_ROOT (si está definido)
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        posibles_ubicaciones.append(os.path.join(settings.STATIC_ROOT, logo_relativo))
    
    # 2. STATICFILES_DIRS (cada directorio)
    if hasattr(settings, 'STATICFILES_DIRS'):
        for static_dir in settings.STATICFILES_DIRS:
            posibles_ubicaciones.append(os.path.join(static_dir, logo_relativo))
    
    # 3. BASE_DIR / 'static'
    if hasattr(settings, 'BASE_DIR'):
        posibles_ubicaciones.append(os.path.join(settings.BASE_DIR, 'static', logo_relativo))
    
    # 4. Dentro de la app 'pagos' (por si acaso)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    posibles_ubicaciones.append(os.path.join(app_dir, 'static', logo_relativo))
    
    # 5. Ruta absoluta directa (por si se pasó la ruta completa)
    posibles_ubicaciones.append(logo_relativo)
    
    # Recorrer todas las ubicaciones y devolver la primera que exista
    for ruta in posibles_ubicaciones:
        if os.path.exists(ruta):
            return ruta
    
    # No se encontró el logo
    return None


# ========== FUNCIÓN PRINCIPAL PARA GENERAR EL PDF ==========
def generar_factura_pdf(reserva_id):
    """
    Genera un PDF de factura para la reserva con ID reserva_id.
    Retorna un objeto BytesIO con el contenido del PDF.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    # Obtener la reserva
    try:
        reserva = Reserva.objects.get(id=reserva_id)
    except Reserva.DoesNotExist:
        return None

    # ========== CÁLCULOS ==========
    duracion_texto = reserva.duracion.lower()
    if 'hora' in duracion_texto:
        horas = Decimal(duracion_texto.split()[0])
    elif 'min' in duracion_texto:
        minutos = Decimal(duracion_texto.split()[0])
        horas = minutos / 60
    else:
        horas = Decimal(1)

    subtotal = PRECIO_POR_HORA * horas
    iva = subtotal * Decimal('0.19')
    total = subtotal + iva

    anio = reserva.fecha.strftime('%Y')
    mes = reserva.fecha.strftime('%m')
    num_factura = f"FAC-{anio}-{mes}-{reserva.id:04d}"

    # ========== ESTILOS ==========
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLOR_VERDE_OSCURO,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    estilo_normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_NEGRO,
    )
    estilo_negrita = ParagraphStyle(
        'Negrita',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_NEGRO,
        fontName='Helvetica-Bold',
    )
    estilo_encabezado_tabla = ParagraphStyle(
        'EncabezadoTabla',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_BLANCO,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
    )
    estilo_celda_tabla = ParagraphStyle(
        'CeldaTabla',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLOR_NEGRO,
        alignment=TA_CENTER,
    )
    estilo_total = ParagraphStyle(
        'Total',
        parent=styles['Normal'],
        fontSize=12,
        textColor=COLOR_VERDE_OSCURO,
        fontName='Helvetica-Bold',
        alignment=TA_RIGHT,
    )

    # ========== ELEMENTOS DEL PDF ==========
    elementos = []

    # ----- ENCABEZADO: LOGO + DATOS DE LA EMPRESA -----
    logo_path = encontrar_logo()
    
    if logo_path:
        try:
            logo = Image(logo_path, width=1.2 * inch, height=1.2 * inch)
        except Exception as e:
            # Si hay error al cargar la imagen, usamos texto
            logo = Paragraph("CanchaFácil", estilo_titulo)
    else:
        logo = Paragraph("CanchaFácil", estilo_titulo)

    datos_empresa = [
        [Paragraph(f"<b>{EMPRESA['nombre']}</b>", estilo_negrita)],
        [Paragraph(f"NIT: {EMPRESA['nit']}", estilo_normal)],
        [Paragraph(f"Dirección: {EMPRESA['direccion']}", estilo_normal)],
        [Paragraph(f"Tel: {EMPRESA['telefono']}", estilo_normal)],
        [Paragraph(f"Email: {EMPRESA['correo']}", estilo_normal)],
    ]
    tabla_empresa = Table(datos_empresa, colWidths=[3 * inch])
    tabla_empresa.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    encabezado = Table([[logo, tabla_empresa]], colWidths=[1.5 * inch, 4.5 * inch])
    encabezado.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(encabezado)
    elementos.append(Spacer(1, 0.2 * inch))

    # ----- TÍTULO -----
    elementos.append(Paragraph("FACTURA DE RESERVA", estilo_titulo))
    elementos.append(Spacer(1, 0.1 * inch))

    # ----- DATOS DE LA FACTURA -----
    datos_factura = [
        [Paragraph("<b>Número:</b>", estilo_negrita), Paragraph(num_factura, estilo_normal)],
        [Paragraph("<b>Fecha emisión:</b>", estilo_negrita), Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), estilo_normal)],
        [Paragraph("<b>Estado:</b>", estilo_negrita), Paragraph(reserva.estado, estilo_normal)],
        [Paragraph("<b>Método pago:</b>", estilo_negrita), Paragraph("Tarjeta / PSE", estilo_normal)],
    ]
    tabla_datos = Table(datos_factura, colWidths=[1.5 * inch, 4 * inch])
    tabla_datos.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elementos.append(tabla_datos)
    elementos.append(Spacer(1, 0.2 * inch))

    # ----- DATOS DEL CLIENTE -----
    datos_cliente = [
        [Paragraph("<b>Cliente:</b>", estilo_negrita), Paragraph(reserva.nombre, estilo_normal)],
        [Paragraph("<b>Correo:</b>", estilo_negrita), Paragraph(reserva.correo, estilo_normal)],
        [Paragraph("<b>Teléfono:</b>", estilo_negrita), Paragraph(reserva.telefono or "No registrado", estilo_normal)],
    ]
    tabla_cliente = Table(datos_cliente, colWidths=[1.5 * inch, 4 * inch])
    tabla_cliente.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla_cliente)
    elementos.append(Spacer(1, 0.2 * inch))

    # ----- DETALLE DE LA RESERVA (TABLA) -----
    data_tabla = [
        [
            Paragraph("<b>Cancha</b>", estilo_encabezado_tabla),
            Paragraph("<b>Fecha</b>", estilo_encabezado_tabla),
            Paragraph("<b>Hora</b>", estilo_encabezado_tabla),
            Paragraph("<b>Duración</b>", estilo_encabezado_tabla),
            Paragraph("<b>Precio/hora</b>", estilo_encabezado_tabla),
            Paragraph("<b>Subtotal</b>", estilo_encabezado_tabla),
        ],
        [
            Paragraph(reserva.cancha, estilo_celda_tabla),
            Paragraph(reserva.fecha.strftime("%d/%m/%Y"), estilo_celda_tabla),
            Paragraph(reserva.hora.strftime("%I:%M %p"), estilo_celda_tabla),
            Paragraph(f"{horas:.1f} h", estilo_celda_tabla),
            Paragraph(f"${PRECIO_POR_HORA:,.0f}", estilo_celda_tabla),
            Paragraph(f"${subtotal:,.0f}", estilo_celda_tabla),
        ]
    ]

    tabla_detalle = Table(data_tabla, colWidths=[1.8 * inch, 1.2 * inch, 1.2 * inch, 1.0 * inch, 1.2 * inch, 1.5 * inch])
    tabla_detalle.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_VERDE_OSCURO),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_BLANCO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 1), (-1, 1), COLOR_VERDE_CLARO),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla_detalle)
    elementos.append(Spacer(1, 0.2 * inch))

    # ----- RESUMEN -----
    resumen_data = [
        [Paragraph("<b>Subtotal</b>", estilo_negrita), Paragraph(f"${subtotal:,.0f}", estilo_normal)],
        [Paragraph("<b>IVA (19%)</b>", estilo_negrita), Paragraph(f"${iva:,.0f}", estilo_normal)],
        [Paragraph("<b>TOTAL A PAGAR</b>", estilo_total), Paragraph(f"${total:,.0f}", estilo_total)],
    ]
    tabla_resumen = Table(resumen_data, colWidths=[4 * inch, 2 * inch])
    tabla_resumen.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
        ('BACKGROUND', (0, 2), (1, 2), COLOR_VERDE_CLARO),
    ]))
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 0.3 * inch))

    # ----- PIE DE PÁGINA -----
    elementos.append(Paragraph("Gracias por reservar con CanchaFácil.", estilo_normal))
    elementos.append(Spacer(1, 0.1 * inch))
    elementos.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilo_normal))

    # ----- FOOTER (número de página) -----
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(0.75 * inch, 0.5 * inch, f"Página {doc.page}")
        canvas.restoreState()

    doc.build(elementos, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer
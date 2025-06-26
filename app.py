from flask import Flask, render_template, jsonify, send_file
import json
from datetime import datetime
import pandas as pd
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = Flask(__name__)

# Configuración
app.config['JSON_AS_ASCII'] = False  # Para caracteres españoles en JSON

# Datos del proyecto
proyecto_data = {
    "resumen": {
        "total_estudiantes": 23675,
        "total_ue": 158,
        "total_provincias": 6,
        "total_alimentos_tm": 450.4,
        "periodo": "Marzo - Abril 2025",
        "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y")
    },
    "productores": {
        "total": 403,
        "por_tamano": {
            "pequenos": {
                "cantidad": 298,
                "porcentaje": 74.0,
                "hectareas_promedio": 0.8,
                "descripcion": "Agricultura familiar < 1 hectárea"
            },
            "medianos": {
                "cantidad": 87,
                "porcentaje": 21.5,
                "hectareas_promedio": 2.5,
                "descripcion": "Productores de 1-5 hectáreas"
            },
            "grandes": {
                "cantidad": 18,
                "porcentaje": 4.5,
                "hectareas_promedio": 8.0,
                "descripcion": "Productores > 5 hectáreas"
            }
        },
        "impacto_economico": {
            "ingreso_promedio_mensual": 485,
            "incremento_porcentual": 35,
            "familias_beneficiadas": 1612
        }
    },
    "categorias_alimentos": {
        "cereales_granos": {
            "nombre": "Cereales y Granos",
            "porcentaje": 28,
            "productos": ["Arroz", "Quinua", "Avena", "Cebada"],
            "color": "#8B4513"
        },
        "proteinas": {
            "nombre": "Proteínas",
            "porcentaje": 22,
            "productos": ["Fréjol", "Lenteja", "Chocho", "Huevos"],
            "color": "#DC143C"
        },
        "frutas_verduras": {
            "nombre": "Frutas y Verduras",
            "porcentaje": 30,
            "productos": ["Tomate", "Zanahoria", "Brócoli", "Manzana", "Plátano"],
            "color": "#228B22"
        },
        "lacteos": {
            "nombre": "Lácteos",
            "porcentaje": 12,
            "productos": ["Leche", "Queso", "Yogurt"],
            "color": "#4682B4"
        },
        "aceites_grasas": {
            "nombre": "Aceites y Grasas",
            "porcentaje": 8,
            "productos": ["Aceite de girasol", "Mantequilla"],
            "color": "#FFD700"
        }
    },
    "alimento_estrella": {
        "nombre": "Quinua",
        "titulo": "Súper Alimento Ancestral",
        "descripcion": "Rica en proteínas completas, minerales y vitaminas",
        "beneficios": [
            "Alto contenido de proteína (14-18%)",
            "Contiene todos los aminoácidos esenciales",
            "Rica en hierro, magnesio y fibra",
            "Libre de gluten naturalmente",
            "Patrimonio alimentario del Ecuador"
        ],
        "frecuencia_semanal": 3,
        "porciones_servidas": 285600
    },
    "mapa_coordenadas": {
        "Pichincha": {"lat": -0.1807, "lng": -78.4678, "estudiantes": 8345},
        "Bolívar": {"lat": -1.5833, "lng": -79.0000, "estudiantes": 1804},
        "Chimborazo": {"lat": -1.6667, "lng": -78.6500, "estudiantes": 55},
        "Manabí": {"lat": -0.9500, "lng": -80.7000, "estudiantes": 2512},
        "Guayas": {"lat": -2.1962, "lng": -79.8862, "estudiantes": 3816},
        "Santa Elena": {"lat": -2.2267, "lng": -80.8583, "estudiantes": 509},
        "Carchi": {"lat": 0.8117, "lng": -77.7172, "estudiantes": 6488},
        "Imbabura": {"lat": 0.3500, "lng": -78.1167, "estudiantes": 3483},
        "Cañar": {"lat": -2.5588, "lng": -78.9378, "estudiantes": 669}
    },
    "modalidades": {
        "GAD": {
            "estudiantes": 13471,
            "ue": 149,
            "tm_alimentos": 252.9,
            "appe": 9,
            "provincias": ["Carchi", "Imbabura", "Bolívar", "Cañar"],
            "porcentaje_estudiantes": 56.8
        },
        "MINEDUC": {
            "estudiantes": 10204,
            "ue": 9,
            "tm_alimentos": 197.5,
            "appe": 7,
            "provincias": ["Pichincha", "Bolívar", "Chimborazo"],
            "porcentaje_estudiantes": 43.2
        }
    },
    "cobertura_provincial": {
        "Pichincha": {"estudiantes": 8345, "ue": 6, "color": "#0033a1"},
        "Bolívar": {"estudiantes": 1804, "ue": 3, "color": "#007DBC"},
        "Chimborazo": {"estudiantes": 55, "ue": 1, "color": "#FF6B00"},
        "Manabí": {"estudiantes": 2512, "ue": 2, "color": "#0033a1"},
        "Guayas": {"estudiantes": 3816, "ue": 2, "color": "#007DBC"},
        "Santa Elena": {"estudiantes": 509, "ue": 1, "color": "#FF6B00"},
        "Carchi": {"estudiantes": 6488, "ue": 40, "color": "#0033a1"},
        "Imbabura": {"estudiantes": 3483, "ue": 49, "color": "#007DBC"},
        "Cañar": {"estudiantes": 669, "ue": 6, "color": "#FF6B00"}
    },
    "evolucion_mensual": [
        {"mes": "Oct 2024", "estudiantes": 564, "ue": 2, "tm": 7.5},
        {"mes": "Nov 2024", "estudiantes": 10925, "ue": 10, "tm": 45.2},
        {"mes": "Dic 2024", "estudiantes": 10925, "ue": 10, "tm": 48.3},
        {"mes": "Ene 2025", "estudiantes": 14529, "ue": 11, "tm": 89.6},
        {"mes": "Feb 2025", "estudiantes": 17041, "ue": 13, "tm": 112.4},
        {"mes": "Mar 2025", "estudiantes": 10204, "ue": 9, "tm": 135.5},
        {"mes": "Abr 2025", "estudiantes": 10204, "ue": 9, "tm": 135.5}
    ],
    "componentes": {
        "nutricion": {
            "descripcion": "Provisión de comidas escolares caseras con enfoque nutricional",
            "actividades": [
                "Comidas diarias rescatando saberes ancestrales",
                "Actividades de nutrición, salud e higiene",
                "Dotación de equipamiento de cocina",
                "Desarrollo de huertos escolares"
            ],
            "impacto": "100% de estudiantes reciben alimentación nutritiva diaria"
        },
        "fortalecimiento": {
            "descripcion": "Apoyo a productores locales y capacidades institucionales",
            "actividades": [
                "Asistencia técnica a APPE",
                "Registro en SERCOP",
                "Desarrollo de capacidades GAD/MINEDUC",
                "Generación de evidencia"
            ],
            "impacto": "403+ pequeños productores beneficiados"
        }
    },
    "indicadores_clave": [
        {"nombre": "Cobertura", "valor": "100%", "descripcion": "Compras a productores locales"},
        {"nombre": "APPE Activas", "valor": "16", "descripcion": "Asociaciones proveedoras"},
        {"nombre": "Productores", "valor": "403+", "descripcion": "Pequeños agricultores beneficiados"},
        {"nombre": "Días de Atención", "valor": "112", "descripcion": "Promedio por institución"}
    ],
    "logros_destacados": [
        "Implementación exitosa en 2 modalidades territoriales",
        "100% de alimentos comprados a productores locales",
        "Fortalecimiento de 16 APPE en 9 provincias",
        "Capacitación en metodología SHEP a productores",
        "Implementación de aplicativo digital 'Mercadito Nilus'"
    ],
    "timeline": [
        {"fecha": "2023-02-16", "evento": "Firma carta de entendimiento WFP-Gobierno", "tipo": "hito"},
        {"fecha": "2024-06-14", "evento": "Firma Acuerdo Específico MINEDUC-WFP", "tipo": "acuerdo"},
        {"fecha": "2024-09-23", "evento": "Transferencia de recursos MINEDUC", "tipo": "financiero"},
        {"fecha": "2024-10-28", "evento": "Inicio implementación progresiva", "tipo": "operativo"},
        {"fecha": "2025-01-31", "evento": "Firma Enmienda No. 1", "tipo": "acuerdo"},
        {"fecha": "2025-04-30", "evento": "Cierre período reportado", "tipo": "reporte"}
    ]
}

# Rutas principales
@app.route('/')
def index():
    return render_template('dashboard.html', data=proyecto_data)

# API endpoints
@app.route('/api/data')
def get_data():
    return jsonify(proyecto_data)

@app.route('/api/provincial-data')
def get_provincial_data():
    return jsonify(proyecto_data['cobertura_provincial'])

@app.route('/api/evolution-data')
def get_evolution_data():
    return jsonify(proyecto_data['evolucion_mensual'])

@app.route('/api/timeline')
def get_timeline():
    return jsonify(proyecto_data['timeline'])

@app.route('/api/stats/compare')
def compare_modalidades():
    """Endpoint para comparación detallada de modalidades"""
    comparison = {
        "GAD": proyecto_data['modalidades']['GAD'],
        "MINEDUC": proyecto_data['modalidades']['MINEDUC'],
        "comparacion": {
            "diferencia_estudiantes": proyecto_data['modalidades']['GAD']['estudiantes'] - 
                                    proyecto_data['modalidades']['MINEDUC']['estudiantes'],
            "diferencia_ue": proyecto_data['modalidades']['GAD']['ue'] - 
                           proyecto_data['modalidades']['MINEDUC']['ue'],
            "eficiencia_tm_por_estudiante": {
                "GAD": round(proyecto_data['modalidades']['GAD']['tm_alimentos'] / 
                            proyecto_data['modalidades']['GAD']['estudiantes'] * 1000, 2),
                "MINEDUC": round(proyecto_data['modalidades']['MINEDUC']['tm_alimentos'] / 
                               proyecto_data['modalidades']['MINEDUC']['estudiantes'] * 1000, 2)
            }
        }
    }
    return jsonify(comparison)

@app.route('/api/productores')
def get_productores():
    """Endpoint para datos de productores"""
    return jsonify(proyecto_data['productores'])

@app.route('/api/alimentos/categorias')
def get_categorias_alimentos():
    """Endpoint para categorías de alimentos"""
    return jsonify(proyecto_data['categorias_alimentos'])

@app.route('/api/alimentos/estrella')
def get_alimento_estrella():
    """Endpoint para alimento estrella"""
    return jsonify(proyecto_data['alimento_estrella'])

# Exportación a Excel
@app.route('/api/export/excel')
def export_excel():
    try:
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja de resumen
            resumen_df = pd.DataFrame([proyecto_data['resumen']])
            resumen_df.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja de modalidades
            modalidades_data = []
            for modalidad, datos in proyecto_data['modalidades'].items():
                datos_copy = datos.copy()
                datos_copy['modalidad'] = modalidad
                modalidades_data.append(datos_copy)
            modalidades_df = pd.DataFrame(modalidades_data)
            modalidades_df.to_excel(writer, sheet_name='Modalidades', index=False)
            
            # Hoja de productores
            productores_list = []
            for tamano, datos in proyecto_data['productores']['por_tamano'].items():
                datos_copy = datos.copy()
                datos_copy['categoria'] = tamano
                productores_list.append(datos_copy)
            productores_df = pd.DataFrame(productores_list)
            productores_df.to_excel(writer, sheet_name='Productores', index=False)
            
            # Hoja de categorías de alimentos
            alimentos_list = []
            for categoria, datos in proyecto_data['categorias_alimentos'].items():
                datos_copy = {
                    'categoria': datos['nombre'],
                    'porcentaje': datos['porcentaje'],
                    'productos': ', '.join(datos['productos'])
                }
                alimentos_list.append(datos_copy)
            alimentos_df = pd.DataFrame(alimentos_list)
            alimentos_df.to_excel(writer, sheet_name='Categorías Alimentos', index=False)
            
            # Hoja de evolución mensual
            evolucion_df = pd.DataFrame(proyecto_data['evolucion_mensual'])
            evolucion_df.to_excel(writer, sheet_name='Evolución Mensual', index=False)
            
            # Hoja de cobertura provincial
            provincial_data = []
            for provincia, datos in proyecto_data['cobertura_provincial'].items():
                datos_copy = datos.copy()
                datos_copy['provincia'] = provincia
                # Agregar coordenadas si existen
                if provincia in proyecto_data['mapa_coordenadas']:
                    datos_copy['latitud'] = proyecto_data['mapa_coordenadas'][provincia]['lat']
                    datos_copy['longitud'] = proyecto_data['mapa_coordenadas'][provincia]['lng']
                provincial_data.append(datos_copy)
            provincial_df = pd.DataFrame(provincial_data)
            provincial_df.to_excel(writer, sheet_name='Cobertura Provincial', index=False)
            
            # Hoja de indicadores
            indicadores_df = pd.DataFrame(proyecto_data['indicadores_clave'])
            indicadores_df.to_excel(writer, sheet_name='Indicadores Clave', index=False)
            
            # Hoja de timeline
            timeline_df = pd.DataFrame(proyecto_data['timeline'])
            timeline_df.to_excel(writer, sheet_name='Timeline', index=False)
            
            # Hoja de alimento estrella
            alimento_estrella_df = pd.DataFrame([{
                'nombre': proyecto_data['alimento_estrella']['nombre'],
                'titulo': proyecto_data['alimento_estrella']['titulo'],
                'descripcion': proyecto_data['alimento_estrella']['descripcion'],
                'frecuencia_semanal': proyecto_data['alimento_estrella']['frecuencia_semanal'],
                'porciones_servidas': proyecto_data['alimento_estrella']['porciones_servidas'],
                'beneficios': '\n'.join(proyecto_data['alimento_estrella']['beneficios'])
            }])
            alimento_estrella_df.to_excel(writer, sheet_name='Alimento Estrella', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'WFP_Comidas_Escolares_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Exportación a PDF
@app.route('/api/export/pdf')
def export_pdf():
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0033a1'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0033a1'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        # Título principal
        elements.append(Paragraph("Proyecto Comidas Escolares - Ecuador", title_style))
        elements.append(Paragraph(f"Informe del Período: {proyecto_data['resumen']['periodo']}", styles['Normal']))
        elements.append(Spacer(1, 30))
        
        # Resumen ejecutivo
        elements.append(Paragraph("Resumen Ejecutivo", heading_style))
        resumen_data = [
            ['Indicador', 'Valor'],
            ['Total Estudiantes Beneficiados', f"{proyecto_data['resumen']['total_estudiantes']:,}"],
            ['Unidades Educativas', str(proyecto_data['resumen']['total_ue'])],
            ['Provincias de Cobertura', str(proyecto_data['resumen']['total_provincias'])],
            ['Toneladas Métricas de Alimentos', str(proyecto_data['resumen']['total_alimentos_tm'])],
            ['Total Productores', str(proyecto_data['productores']['total'])],
            ['Período del Informe', proyecto_data['resumen']['periodo']]
        ]
        
        t = Table(resumen_data, colWidths=[3*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0033a1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee3ed'))
        ]))
        elements.append(t)
        elements.append(Spacer(1, 30))
        
        # Análisis de Productores
        elements.append(Paragraph("Análisis de Productores Locales", heading_style))
        productores_data = [['Categoría', 'Cantidad', 'Porcentaje', 'Hectáreas Promedio']]
        for tipo, datos in proyecto_data['productores']['por_tamano'].items():
            productores_data.append([
                tipo.capitalize(),
                str(datos['cantidad']),
                f"{datos['porcentaje']}%",
                f"{datos['hectareas_promedio']} ha"
            ])
        
        t3 = Table(productores_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#228B22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e6f7e6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee3ed'))
        ]))
        elements.append(t3)
        elements.append(Spacer(1, 20))
        
        # Impacto económico
        elements.append(Paragraph(f"<b>Impacto Económico:</b> Los productores han incrementado sus ingresos en un {proyecto_data['productores']['impacto_economico']['incremento_porcentual']}%, beneficiando a {proyecto_data['productores']['impacto_economico']['familias_beneficiadas']:,} familias.", styles['Normal']))
        elements.append(Spacer(1, 30))
        
        # Indicadores clave
        elements.append(Paragraph("Indicadores Clave de Desempeño", heading_style))
        kpi_data = [['Indicador', 'Valor', 'Descripción']]
        for kpi in proyecto_data['indicadores_clave']:
            kpi_data.append([kpi['nombre'], kpi['valor'], kpi['descripcion']])
        
        t2 = Table(kpi_data, colWidths=[1.5*inch, 1*inch, 3*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6B00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fff5e6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee3ed'))
        ]))
        elements.append(t2)
        elements.append(Spacer(1, 30))
        
        # Alimento Estrella
        elements.append(Paragraph("Alimento Estrella del Mes", heading_style))
        elements.append(Paragraph(f"<b>{proyecto_data['alimento_estrella']['nombre']}</b> - {proyecto_data['alimento_estrella']['titulo']}", styles['Normal']))
        elements.append(Paragraph(proyecto_data['alimento_estrella']['descripcion'], styles['Normal']))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("Beneficios:", styles['Normal']))
        for beneficio in proyecto_data['alimento_estrella']['beneficios'][:3]:  # Solo los primeros 3 para el PDF
            elements.append(Paragraph(f"• {beneficio}", styles['Normal']))
        elements.append(Spacer(1, 30))
        
        # Logros destacados
        elements.append(Paragraph("Logros Destacados", heading_style))
        for i, logro in enumerate(proyecto_data['logros_destacados'], 1):
            elements.append(Paragraph(f"{i}. {logro}", styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'WFP_Informe_Comidas_Escolares_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
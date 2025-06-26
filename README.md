# Dashboard WFP - Proyecto Comidas Escolares Ecuador

## 📊 Descripción

Dashboard ejecutivo interactivo para el Proyecto de Comidas Escolares del Programa Mundial de Alimentos (WFP) en Ecuador. Visualiza datos de 23,675 estudiantes beneficiados en 158 unidades educativas durante el período Marzo-Abril 2025.

## 🚀 Características

- **Diseño Moderno**: Interfaz profesional con la línea gráfica del WFP
- **Visualizaciones Interactivas**: Gráficos dinámicos con Chart.js
- **Exportación de Datos**: Descarga en Excel y PDF
- **API REST**: Endpoints para integración con otros sistemas
- **Responsive**: Adaptado para todos los dispositivos
- **Animaciones**: Transiciones suaves y efectos visuales

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
# Crear directorio del proyecto
mkdir wfp-dashboard
cd wfp-dashboard
```

### 2. Crear la estructura de carpetas

```bash
# Crear directorios necesarios
mkdir templates
mkdir -p static/css
mkdir -p static/js
mkdir data
```

### 3. Copiar los archivos

Coloca cada archivo en su ubicación correspondiente:
- `app.py` en la raíz
- `dashboard.html` en `templates/`
- `styles.css` en `static/css/`
- `dashboard.js` en `static/js/`
- `requirements.txt` en la raíz

### 4. Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Ejecución

### Modo desarrollo

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

### Modo producción

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📁 Estructura del Proyecto

```
wfp-dashboard/
│
├── app.py                    # Aplicación Flask principal
├── requirements.txt          # Dependencias Python
├── README.md                # Este archivo
│
├── templates/               # Plantillas HTML
│   └── dashboard.html       # Dashboard principal
│
├── static/                  # Archivos estáticos
│   ├── css/
│   │   └── styles.css      # Estilos CSS
│   └── js/
│       └── dashboard.js     # JavaScript del dashboard
│
└── data/                    # (Opcional) Archivos de datos
```

## 🔌 API Endpoints

### Datos Generales
```
GET /api/data
```
Retorna todos los datos del proyecto en formato JSON

### Datos Provinciales
```
GET /api/provincial-data
```
Retorna datos de cobertura por provincia

### Evolución Temporal
```
GET /api/evolution-data
```
Retorna la evolución mensual de beneficiarios

### Timeline del Proyecto
```
GET /api/timeline
```
Retorna los hitos principales del proyecto

### Comparación de Modalidades
```
GET /api/stats/compare
```
Retorna comparación detallada entre GAD y MINEDUC

### Exportar a Excel
```
GET /api/export/excel
```
Descarga archivo Excel con todos los datos

### Exportar a PDF
```
GET /api/export/pdf
```
Descarga informe en formato PDF

## 🎨 Personalización

### Actualizar Datos

Los datos están centralizados en `app.py` en el diccionario `proyecto_data`:

```python
proyecto_data = {
    "resumen": {
        "total_estudiantes": 23675,  # Actualizar aquí
        "total_ue": 158,
        # ... más datos
    }
}
```

### Modificar Colores

Editar las variables CSS en `static/css/styles.css`:

```css
:root {
    --wfp-blue: #0033a1;      /* Color principal */
    --wfp-orange: #FF6B00;    /* Color secundario */
    /* ... más colores */
}
```

### Agregar Nuevos Gráficos

1. Añadir contenedor en `dashboard.html`:
```html
<div class="chart-container">
    <h3 class="chart-title">Nuevo Gráfico</h3>
    <canvas id="nuevoChart"></canvas>
</div>
```

2. Crear función en `dashboard.js`:
```javascript
const createNuevoChart = () => {
    // Código del gráfico
};
```

## 🐛 Solución de Problemas

### Error: "Module not found"
Asegúrate de haber instalado todas las dependencias:
```bash
pip install -r requirements.txt
```

### Puerto 5000 en uso
Cambia el puerto en `app.py`:
```python
app.run(debug=True, port=5001)  # Usar puerto 5001
```

### Problemas con exportación PDF
Instalar reportlab manualmente:
```bash
pip install --upgrade reportlab
```

## 📝 Notas de Desarrollo

- El dashboard usa datos estáticos definidos en `app.py`
- Para producción, considera usar una base de datos
- Los gráficos se renderizan con Chart.js v3
- Compatible con Chrome, Firefox, Safari y Edge

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto fue desarrollado para el Programa Mundial de Alimentos - Ecuador.

## 📞 Contacto

Para preguntas o soporte técnico sobre el dashboard, contactar al equipo de desarrollo.

---

**Programa Mundial de Alimentos**  
*Salvando vidas, cambiando vidas*
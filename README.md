# Sistema de Pedidos - CRUD Web

Sistema web completo con Python (Flask) para gestión de pedidos con upload de imágenes y exportación a Excel.

## Características

- CRUD completo de pedidos
- Campos: pedido, teléfono, folio, prepó, empacó, situación, solución, status
- Status en ComboBox (Pendiente, En Proceso, Completado, Cancelado)
- Fecha automática según zona horaria de Ciudad de México
- Múltiples imágenes por pedido
- Visualización de imágenes en grande
- Buscador en tiempo real
- Exportación a Excel
- Base de datos SQLite

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:
```bash
python app.py
```

2. Abrir navegador en: http://localhost:5000

## Estructura del Proyecto

```
sistema_crud/
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración
├── database.py         # Modelos de base de datos
├── requirements.txt    # Dependencias
├── static/
│   └── uploads/        # Imágenes subidas
└── templates/
    └── index.html      # Dashboard principal
```

## Campos del Formulario

| Campo | Descripción | Tipo |
|-------|-------------|------|
| Pedido | Nombre del pedido | Texto |
| Teléfono | Número de contacto | Texto |
| Folio | Número de folio | Texto |
| Prepró | Nombre de quien prepró | Texto |
| Empacó | Nombre de quien empacó | Texto |
| Situación | Descripción de la situación | Texto |
| Solución | Solución aplicada | Texto |
| Status | Estado del pedido | ComboBox |
| Imágenes | Evidencia fotográfica | Múltiples archivos |

## API Endpoints

- `GET /` - Dashboard principal
- `GET /api/pedidos` - Listar pedidos (soporta ?busqueda=)
- `POST /api/pedidos` - Crear pedido
- `GET /api/pedidos/<id>` - Obtener pedido
- `PUT /api/pedidos/<id>` - Actualizar pedido
- `DELETE /api/pedidos/<id>` - Eliminar pedido
- `POST /api/pedidos/<id>/imagenes` - Subir imágenes
- `DELETE /api/imagenes/<id>` - Eliminar imagen
- `GET /api/exportar-excel` - Exportar a Excel

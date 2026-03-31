from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime, timezone, timedelta
import os
import pandas as pd
from config import Config
from database import db, init_db, Pedido, Imagen

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_fecha_mexico():
    tz_mexico = timezone(timedelta(hours=-6))
    return datetime.now(tz_mexico)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    busqueda = request.args.get('busqueda', '')
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)
    
    query = Pedido.query
    
    if busqueda:
        search = f'%{busqueda}%'
        query = query.filter(
            (Pedido.pedido.like(search)) |
            (Pedido.telefono.like(search)) |
            (Pedido.folio.like(search)) |
            (Pedido.preparo.like(search)) |
            (Pedido.empaco.like(search)) |
            (Pedido.situacion.like(search)) |
            (Pedido.solucion.like(search)) |
            (Pedido.status.like(search))
        )
    
    total = query.count()
    pedidos = query.order_by(Pedido.fecha_creacion.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
    
    return jsonify({
        'pedidos': [p.to_dict() for p in pedidos],
        'total': total,
        'pagina': pagina,
        'por_pagina': por_pagina,
        'total_paginas': (total + por_pagina - 1) // por_pagina if total > 0 else 1
    })

@app.route('/api/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()
    
    fecha_mexico = get_fecha_mexico()
    
    pedido = Pedido(
        pedido=data.get('pedido'),
        telefono=data.get('telefono'),
        folio=data.get('folio'),
        preparo=data.get('preparo'),
        empaco=data.get('empaco'),
        situacion=data.get('situacion'),
        solucion=data.get('solucion'),
        status=data.get('status', 'Pendiente'),
        fecha_creacion=fecha_mexico
    )
    
    db.session.add(pedido)
    db.session.commit()
    
    return jsonify(pedido.to_dict()), 201

@app.route('/api/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    return jsonify(pedido.to_dict())

@app.route('/api/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    
    data = request.get_json()
    
    pedido.pedido = data.get('pedido', pedido.pedido)
    pedido.telefono = data.get('telefono', pedido.telefono)
    pedido.folio = data.get('folio', pedido.folio)
    pedido.preparo = data.get('preparo', pedido.preparo)
    pedido.empaco = data.get('empaco', pedido.empaco)
    pedido.situacion = data.get('situacion', pedido.situacion)
    pedido.solucion = data.get('solucion', pedido.solucion)
    pedido.status = data.get('status', pedido.status)
    pedido.fecha_actualizacion = get_fecha_mexico()
    
    db.session.commit()
    
    return jsonify(pedido.to_dict())

@app.route('/api/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    
    for img in pedido.imagenes:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], img.nombre_archivo)
        if os.path.exists(img_path):
            os.remove(img_path)
    
    db.session.delete(pedido)
    db.session.commit()
    
    return jsonify({'message': 'Pedido eliminado'})

@app.route('/api/pedidos/<int:id>/imagenes', methods=['POST'])
def upload_images(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    
    if 'files' not in request.files:
        return jsonify({'error': 'No se enviaron archivos'}), 400
    
    files = request.files.getlist('files')
    uploaded_images = []
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            imagen = Imagen(
                nombre_archivo=unique_filename,
                pedido_id=pedido.id
            )
            db.session.add(imagen)
            uploaded_images.append(imagen)
    
    db.session.commit()
    
    return jsonify([img.to_dict() for img in uploaded_images]), 201

@app.route('/api/imagenes/<int:id>', methods=['DELETE'])
def delete_image(id):
    imagen = Imagen.query.get(id)
    if not imagen:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.nombre_archivo)
    if os.path.exists(img_path):
        os.remove(img_path)
    
    db.session.delete(imagen)
    db.session.commit()
    
    return jsonify({'message': 'Imagen eliminada'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/exportar-excel')
def export_excel():
    pedidos = Pedido.query.order_by(Pedido.fecha_creacion.desc()).all()
    
    data = []
    for p in pedidos:
        imagenes = ', '.join([img.nombre_archivo for img in p.imagenes])
        data.append({
            'ID': p.id,
            'Pedido': p.pedido,
            'Telefono': p.telefono,
            'Folio': p.folio,
            'Prepro': p.preparo,
            'Empaco': p.empaco,
            'Situacion': p.situacion,
            'Solucion': p.solucion,
            'Status': p.status,
            'Fecha Creacion': p.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if p.fecha_creacion else '',
            'Imagenes': imagenes
        })
    
    df = pd.DataFrame(data)
    
    fecha_mexico = get_fecha_mexico()
    filename = f'pedidos_export_{fecha_mexico.strftime("%Y%m%d_%H%M%S")}.xlsx'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return jsonify({'download_url': url_for('uploaded_file', filename=filename)})

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True, host='192.168.1.95', port=5000)
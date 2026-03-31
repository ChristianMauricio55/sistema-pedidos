from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask import url_for  # 🔥 AQUÍ

db = SQLAlchemy()

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    folio = db.Column(db.String(50), nullable=True)
    preparo = db.Column(db.String(100), nullable=True)
    empaco = db.Column(db.String(100), nullable=True)
    situacion = db.Column(db.Text, nullable=True)
    solucion = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pendiente')
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    imagenes = db.relationship('Imagen', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido': self.pedido,
            'telefono': self.telefono,
            'folio': self.folio,
            'preparo': self.preparo,
            'empaco': self.empaco,
            'situacion': self.situacion,
            'solucion': self.solucion,
            'status': self.status,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_actualizacion else None,
            'imagenes': [img.to_dict() for img in self.imagenes]
        }

class Imagen(db.Model):
    __tablename__ = 'imagenes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'pedido_id': self.pedido_id,
            'fecha_subida': self.fecha_subida.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_subida else None
        }

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy(app)

class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(3), nullable=False)
    autor_nombre = db.Column(db.String(100), nullable=False)
    autor_apellido = db.Column(db.String(100), nullable=False)
    autor_email = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente') 
    fecha_envio = db.Column(db.DateTime, default=datetime.now)
    archivo_nombre = db.Column(db.String(255), nullable=True)        
    asignaciones = db.relationship('Asignacion', backref='trabajo', lazy=True)
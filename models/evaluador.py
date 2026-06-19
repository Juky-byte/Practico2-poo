from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy(app)

class Evaluador(db.Model):
    __tablename__ = 'evaluadores'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(5))
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    area = db.Column(db.String(3), nullable=False)    
    max_trabajos = db.Column(db.Integer, nullable=False, default=3)
    clave = db.Column(db.String(100), nullable=False)        
    asignaciones = db.relationship('Asignacion', backref='evaluador', lazy=True)
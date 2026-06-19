from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy(app)

class Organizador(db.Model):
    __tablename__ = 'organizadores'
    id = db.Column(db.Integer, primary_key=True)    
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(100), nullable=False)
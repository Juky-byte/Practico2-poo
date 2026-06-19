from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy(app)
class Asignacion(db.Model):
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, db.ForeignKey('trabajos.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('evaluadores.id'), nullable=False)
    valoracion = db.Column(db.Integer, nullable=True) 
    comentarios = db.Column(db.Text, nullable=True)
    fecha_evaluacion = db.Column(db.DateTime, nullable=True)
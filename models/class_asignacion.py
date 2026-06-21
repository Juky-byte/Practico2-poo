from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

class Asignacion(db.Model):
    # atributos:
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key = True)
    trabajo_id = db.Column(db.Integer, db.ForeignKey('trabajos.id'), nullable = False) #clave foranea
    evaluador_id = db.Column(db.Integer, db.ForeignKey('evaluadores.id'), nullable = False) #clave foranea
    valoracion = db.Column(db.Integer, nullable = True) 
    comentarios = db.Column(db.Text, nullable = True)
    fecha_evaluacion = db.Column(db.DateTime, nullable = True)

    # consultas:
    def get_id(self):
        return self.id
    
    def get_trabajo_id(self):
        return self.trabajo_id
    
    def get_evaluador_id(self):
        return self.evaluador_id
    
    def get_valoracion(self):
        return self.valoracion
    
    def get_comentarios(self):
        return self.comentarios
    
    def get_fecha_evaluacion(self):
        if self.fecha_evaluacion != None:
            return self.fecha_evaluacion.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return self.fecha_evaluacion
        
from app import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

class Evaluador(db.Model):
    # atributos:
    __tablename__ = 'evaluadores'
    id = db.Column(db.Integer, primary_key = True) #clave primaria
    titulo = db.Column(db.String(5))
    nombre = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(50), nullable = False)
    correo = db.Column(db.String(120), unique = True, nullable = False)
    area = db.Column(db.String(3), nullable = False)    
    max_trabajos = db.Column(db.Integer, nullable = False, default = 3)
    clave = db.Column(db.String(100), nullable = False)        
    asignaciones =  db.relationship('Asignacion', backref = 'evaluador', lazy = True)

    # consultas:
    def get_id(self):
        return self.id
    
    def get_titulo(self):
        return self.titulo
    
    def get_nombre(self):
        return self.nombre
    
    def get_apellido(self):
        return self.apellido
    
    def get_correo(self):
        return self.correo
    
    def get_area(self):
        return self.area
    
    def get_max_trabajos(self):
        return self.max_trabajos
    
    def get_clave(self):
        return self.clave
    
    def get_asignaciones(self): 
        return self.asignaciones
    
    def verifica_clave(self,contra):
        return check_password_hash(self.clave, contra)
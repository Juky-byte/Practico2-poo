from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

class Trabajo(db.Model):
    # atributos:
    __tablename__ = 'trabajos'
    id = db.Column(db.Integer, primary_key = True) #clave primaria
    titulo = db.Column(db.String(200), nullable = False)
    resumen = db.Column(db.Text, nullable = False)
    area = db.Column(db.String(3), nullable = False)
    autor_nombre = db.Column(db.String(100), nullable = False)
    autor_apellido = db.Column(db.String(100), nullable = False)
    autor_email = db.Column(db.String(120), nullable = False)
    estado = db.Column(db.String(20), default = 'Pendiente') 
    fecha_envio = db.Column(db.DateTime, default = datetime.now)
    archivo_nombre = db.Column(db.String(255), nullable = True)        
    asignaciones = db.relationship('Asignacion', backref = 'trabajo', lazy = True)

    # consultas:
    def get_id(self):
        return self.id
    
    def get_titulo(self):
        return self.titulo
    
    def get_resumen(self):
        return self.resumen
    
    def get_area(self):
        return self.area
    
    def get_autor_nombre(self):
        return self.autor_nombre
    
    def get_autor_apellido(self):
        return self.autor_apellido
    
    def get_autor_email(self):
        return self.autor_email
    
    def get_estado(self):
        return self.estado
    
    def set_estado(self,otro):
        self.estado = otro
    
    def get_fecha_envio(self):
        return self.fecha_envio.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_archivo_nombre(self):
        return self.archivo_nombre
    
    def get_asignaciones(self): 
        return self.asignaciones 
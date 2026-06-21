from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy(app)

class Organizador(db.Model):
    __tablename__ = 'organizadores'
    id = db.Column(db.Integer, primary_key = True)  #clave primaria    
    nombre = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(50), nullable = False)
    correo = db.Column(db.String(120), unique = True, nullable = False)
    clave = db.Column(db.String(100), nullable = False)

    def get_id(self):
        return self.id
    
    def get_nombre(self):
        return self.nombre
    
    def get_apellido(self):
        return self.apellido
    
    def get_correo(self):
        return self.correo
    
    def get_clave(self):
        return self.clave
    
    def verifica_clave(self,contra):
        return check_password_hash(self.clave, contra)
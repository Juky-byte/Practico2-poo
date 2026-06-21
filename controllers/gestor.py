from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session
from models import Trabajo, Evaluador, Asignacion, Organizador
from app import db

class GestorDB:
    # constructor:
    def crearDB(self):
        db.create_all()

    # operaciones:
    def crear_trabajo(self, titulo, resumen, area, autor_nombre, autor_apellido, autor_email, archivo):
        nuevo_trabajo = Trabajo(
            titulo = titulo,
            resumen = resumen,
            area = area,
            autor_nombre = autor_nombre,
            autor_apellido = autor_apellido,
            autor_email = autor_email,   
            archivo_nombre = archivo,
            estado = "Pendiente",
            fecha_envio = datetime.now()
        )
        if not nuevo_trabajo.id:    
            db.session.add(nuevo_trabajo)
            db.session.commit()
        
        return nuevo_trabajo.id
   
    # consultas:
    def get_trabajo(self,id_trabajo, correo_autor):
        trabajo = db.session.query(Trabajo).filter(
            Trabajo.id == id_trabajo,
            Trabajo.autor_email == correo_autor
        ).first()
        return trabajo


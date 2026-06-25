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
    
    def asignar_trabajos(self):
        trabajos = Trabajo.query.filter_by(estado="Pendiente").all()
        detalles_asignaciones = []
        for trabajo in trabajos:
            area_trabajo = trabajo.get_area().strip()
            evaluadores = Evaluador.query.filter(Evaluador.area.like(f"{area_trabajo}%")).all()
            count = 0
            i = 0
            hubo_cambio_trabajo = False
            while i < len(evaluadores) and count < 3:
                evaluador_actual = evaluadores[i]  
                # Consultar cupo
                cant_actual = db.session.query(Asignacion).filter_by(evaluador_id=evaluador_actual.get_id()).count()
                tiene_cupo = cant_actual < evaluador_actual.get_max_trabajos() 
                # Evitar duplicados
                ya_asignado = False
                lista_asig = trabajo.get_asignaciones()
                j = 0
                while j < len(lista_asig):
                    if lista_asig[j].get_evaluador_id() == evaluador_actual.get_id():
                        ya_asignado = True
                    j += 1
                if tiene_cupo and not ya_asignado:
                    nueva_asignacion = Asignacion(trabajo_id=trabajo.get_id(), evaluador_id=evaluador_actual.get_id())
                    db.session.add(nueva_asignacion)
                    detalles_asignaciones.append({
                        'trabajo_titulo': trabajo.get_titulo(),
                        'evaluador_nombre': f"{evaluador_actual.get_apellido()}, {evaluador_actual.get_nombre()}",
                        'area': trabajo.get_area()
                    })
                    count += 1
                    hubo_cambio_trabajo = True
                i += 1
            if hubo_cambio_trabajo:
                trabajo.set_estado("Asignado")   
        db.session.commit()
        return detalles_asignaciones

    def Evaluadas(self, evaluador_id):
        asignaciones = Asignacion.query.filter_by(evaluador_id=evaluador_id).all()
        evaluadas = []
        i = 0
        while i < len(asignaciones):
            asignacion = asignaciones[i]
            if asignacion.fue_evaluada():
                evaluadas.append(asignacion)
            i += 1
        return evaluadas
    
    def Pendientes(self, evaluador_id):
        asignaciones = Asignacion.query.filter_by(evaluador_id=evaluador_id).all()
        pendientes = []
        i = 0
        while i < len(asignaciones):
            asignacion = asignaciones[i]
            if not asignacion.fue_evaluada():
                pendientes.append(asignacion)
            i += 1
        return pendientes
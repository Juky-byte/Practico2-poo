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
        print(f"\n=== [DIAGNÓSTICO] Cantidad de trabajos pendientes encontrados: {len(trabajos)} ===")
        for trabajo in trabajos:
            # Limpiamos el código de área quitando espacios
            area_trabajo = trabajo.get_area().strip()
            print(f"\n-> Procesando Trabajo ID {trabajo.get_id()}: '{trabajo.get_titulo()}' | Área: '{area_trabajo}'")
            # Buscamos evaluadores cuyos primeros caracteres coincidan con el área
            evaluadores = Evaluador.query.filter(Evaluador.area.like(f"{area_trabajo}%")).all()
            print(f"   Evaluadores encontrados en la base de datos para esta área: {len(evaluadores)}")
            # Ordenamos consultando la base de datos limpiamente
            evaluadores = sorted(evaluadores, key=lambda e: db.session.query(Asignacion).filter_by(evaluador_id=e.get_id()).count())
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
                print(f"   - Evaluador: {evaluador_actual.get_nombre()} {evaluador_actual.get_apellido()} | Cupo Actual: {cant_actual}/{evaluador_actual.get_max_trabajos()} (Tiene cupo: {tiene_cupo}) | Ya asignado antes: {ya_asignado}") 
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
                    print(f"     [¡ASIGNADO CORECTAMENTE!]")
                i += 1
            if hubo_cambio_trabajo:
                trabajo.set_estado("Asignado")   
        db.session.commit()
        print(f"\n=== [FIN DIAGNÓSTICO] Asignaciones totales creadas en este clic: {len(detalles_asignaciones)} ===\n")
        return detalles_asignaciones

import os
from flask import Flask, request, render_template, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
from werkzeug.security import check_password_hash
# inicializo la aplicacion
app = Flask(__name__)
app.config.from_object(Config)

# crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok = True)

# inicializo una instancia de la base de datos que va a ser compartida en los demas modulos
db = SQLAlchemy(app)

# se crea el gestor de la app
from controllers.gestor import GestorDB
gestor = GestorDB()
from models.class_evaluador import Evaluador
from models.class_organizador import Organizador
from models.class_asignacion import Asignacion
from models.class_trabajo import Trabajo

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login(): # Esto es una vista
    if request.method == 'POST':
        correo_ingresado = request.form.get('correo')
        clave_ingresada = request.form.get('clave')
        evaluador = Evaluador.query.filter_by(correo=correo_ingresado).first()
        organizador = Organizador.query.filter_by(correo=correo_ingresado).first()

        if evaluador and check_password_hash(evaluador.get_clave(), clave_ingresada):
            session['rol'] = 'evaluador'
            session['correo'] = evaluador.get_correo()
            session['nombre'] = evaluador.get_nombre()
            session['apellido'] = evaluador.get_apellido()
            session['id'] = evaluador.id
            flash(f'¡Bienvenido {evaluador.get_nombre()}!', 'exito')
            resultado = redirect(url_for('bandeja'))
        elif organizador and check_password_hash(organizador.get_clave(), clave_ingresada):
            session['rol'] = 'organizador'
            session['correo'] = organizador.get_correo()
            session['nombre'] = organizador.get_nombre()
            session['apellido'] = organizador.get_apellido()
            session['id'] = organizador.id
            flash(f'¡Bienvenido {organizador.get_nombre()}!', 'exito')
            resultado = redirect(url_for('asignar_trabajos'))   
        else:
            flash('Correo o contraseña incorrectos', 'error')
            resultado = redirect(url_for('login'))
    else:
        resultado = render_template('login.html')  
    return resultado

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('login'))

@app.route('/limpiar')
def limpiar_sesion():
    session.clear()  # Borra el rol y el ID viejo por completo
    print("\n=== ¡SESIÓN BORRADA EN EL SERVIDOR! ===\n")
    return "Sesión limpia. Ahora ve a /login e intenta ingresar de nuevo."

@app.route('/bienvenida', methods = ['POST'])
def bienvenida():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        rol_elegido = request.form.get('rol')
        session['nombre'] = nombre
        session['email'] = email
        session['rol'] = rol_elegido
        flash(f"¡Inicio de sesión exitoso como {rol_elegido.capitalize()}!", "success")
        retorno = redirect(url_for('inicio'))
    else:
        retorno = render_template('error.html')
    return retorno # Redirige al inicio o home

#Funcionalidad 1
@app.route("/enviar_trabajo", methods = ['GET', 'POST'])
def enviar_trabajo():
    resultado = ""
    if request.method == 'POST':
        titulo = request.form['titulo']
        resumen = request.form['resumen']
        area = request.form['area']
        autor_nombre = request.form['autor_nombre']
        autor_apellido = request.form['autor_apellido']
        autor_email = request.form['autor_email']
        archivo = request.files['archivo']
        # guardar archivo en carpeta uploads
        if archivo:
            ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            archivo.save(ruta_archivo)
        # guardar usando el gestor
        id = gestor.crear_trabajo(titulo, resumen, area, autor_nombre, autor_apellido, autor_email, archivo.filename)
        resultado = render_template('aviso.html', message = f"Trabajo enviado correctamente. ID asignado: {id}")
    else: # si entra por GET, muestra el formulario
        resultado = render_template('enviar_trabajo.html')
    return resultado

# Funcionalidad 2
@app.route("/consultar_trabajo",methods = ['GET', 'POST'])
def consultar_trabajo():
    resultado = ''
    if request.method == 'POST':
        id_trabajo = request.form.get('id_trabajo')
        correo = request.form.get('autor_email')
        trabajo = gestor.get_trabajo(id_trabajo,correo)
        if trabajo:
            resultado = render_template(
                "consultar_trabajo.html",
                trabajo_1 = trabajo,
                mensaje ='Codigo es:'
            )
        else:
            resultado = render_template(
                "consultar_trabajo.html",
                trabajo_1 = None,
                mensaje = "No se encontró un trabajo con esos datos."
            )
    else:
        resultado = render_template("consultar_trabajo.html", trabajo_1 = None, mensaje = None)
    return resultado

# Funcionalidad 3
@app.route("/asignar_trabajos")
def asignar_trabajos():
    asignaciones = gestor.asignar_trabajos()
    retorno = render_template('asignar_trabajo.html', asignaciones = asignaciones)
    return retorno

# Funcionalidad 5
@app.route('/bandeja')
def bandeja():
    if session.get('rol') == 'Organizador':
        resultado = render_template('error.html')
    else:
        pendientes = gestor.Pendientes(session.get('id'))
        evaluadas_lista = gestor.Evaluadas(session.get('id'))
        
        resultado = render_template('bandeja.html', pendientes=pendientes, evaluadas=evaluadas_lista)
    return resultado

if __name__ == '__main__':
    with app.app_context(): # le digo a python que actúe como si la app estuviera corriendo(realmente no lo hace)
        gestor.crearDB()
        app.run(debug = True,port = 5000) #Se ejecuta la aplicación, "debug" por defecto es False, puerto 5000 (se puede modificar)
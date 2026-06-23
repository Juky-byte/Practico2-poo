import os
from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

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

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login') #se decora con "/" indicando que va a estar ligada a la ruta raíz
def login(): #Esto es una vista
    #return "Todavía no hay nada..."
    return render_template('login.html')  #va la plantilla que va estar ubicada en Html

@app.route("/bienvenida", methods = ['POST', 'GET'])
def bienvenida():
    resultado = ""
    if request.method == 'POST':
        if request.form['nombre'] and request.form['email'] and request.form['password'] and request.form['rol']:
            datosf = request.form
            if request.form['rol'] == 'evaluador':
                resultado = render_template('bienvenida.html', datos = datosf, hora = datetime.now().hour) #CAMBIAR A LO QUE DEBE A HACER
            elif request.form['rol'] == 'organizador':
                resultado = render_template('bienvenida.html', datos = datosf, hora = datetime.now().hour) #CAMBIAR A LO QUE DEBE A HACER
        else:
            resultado = render_template('login.html')
    else:
        resultado = render_template('error.html')
    return resultado

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
        id = gestor.agregar_trabajo(titulo, resumen, area, autor_nombre, autor_apellido, autor_email, archivo.filename)
        resultado = render_template('aviso.html', message = f"Trabajo enviado correctamente. ID asignado: {id}")
    else: # si entra por GET, muestra el formulario
        resultado = render_template('enviar_trabajo.html')
    return resultado

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

if __name__ == '__main__':
    with app.app_context(): # le digo a python que actúe como si la app estuviera corriendo(realmente no lo hace)
        gestor.crearDB()
        app.run(debug = True,port = 5000) #Se ejecuta la aplicación, "debug" por defecto es False, puerto 5000 (se puede modificar)
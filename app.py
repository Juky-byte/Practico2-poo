from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)  #Inicializo la aplicación
@app.route('/') #se decora con "/" indicando que va a estar ligada a la ruta raíz
def index(): #Esto es una vista
    #return "Todavía no hay nada..."
    return render_template('login.html')  #va la plantilla que va estar ubicada en Html

@app.route("/bienvenida", methods = ['POST', 'GET'])
def bienvenida():
    resultado = ""
    if request.method == 'POST':
        if request.form['nombre'] and request.form['email'] and request.form['password']:
            datosf = request.form
            resultado = render_template('bienvenida.html', datos = datosf, hora = datetime.now().hour)
        else:
            resultado = render_template('login.html')
    else:
        resultado = render_template('error.html')
    return resultado

if __name__ == '__main__':
    with app.app_context(): #le digo a python que actúe como si la app estuviera corriendo(realmente no lo hace)
        app.run(debug = True,port = 5000) #Se ejecuta la aplicación, "debug" por defecto es False, puerto 5000 (se puede modificar)
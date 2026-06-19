from flask import Flask, render_template

app = Flask(__name__)  #Inicializo la aplicación
@app.route('/') #se decora con "/" indicando que va a estar ligada a la ruta raíz
def index(): #Esto es una vista
    #return "Todavía no hay nada..."
    return render_template('')  #va la plantilla que va estar ubicada en Html
if __name__ == '__main__':
    app.run(debug = False,port = 5000) #Se ejecuta la aplicación, "debug" por defecto es False, puerto 5000 (se puede modificar)
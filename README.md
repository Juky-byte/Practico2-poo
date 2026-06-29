# Practico2-poo
Aplicacion web para programacion orientada a objetos
# ETI - Evaluación de Trabajos de Investigación

## 📖 Descripción
Sistema web desarrollado en Flask para gestionar la carga, consulta y evaluación de trabajos de investigación en un congreso académico.  
Permite a los **autores** enviar trabajos, a los **organizadores** asignar evaluadores automáticamente y a los **evaluadores** revisar y calificar los trabajos.

---

## 🛠️ Tecnologías utilizadas
- Python 3.x
- Flask
- SQLAlchemy
- HTML, CSS (centralizado en `static/css/estilos.css`)
- Jinja2 Templates
- SQLite (base de datos local)

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Juky-byte/Practico2-poo.git
   cd Practico2-poo
Crear entorno virtual:

bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Instalar dependencias:

bash
pip install -r requirements.txt
Configurar variables de entorno en .env:

Código
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta
🚀 Uso
Inicializar la base de datos (si no existe):

bash
flask shell
>>> from app import db
>>> db.create_all()
Ejecutar la aplicación:

bash
flask run
Abrir en el navegador:

Código
http://127.0.0.1:5000

📂 Funcionalidades principales
Inicio de sesión con roles: Autor, Organizador, Evaluador.

Enviar trabajo: formulario para subir título, área y archivo.

Consultar trabajo: búsqueda por ID y correo.

Asignación automática: el organizador distribuye trabajos pendientes entre evaluadores.

Bandeja del evaluador: lista de trabajos pendientes y evaluados.

Mensajes flash: feedback visual para acciones (login, errores, confirmaciones).

📁 Estructura del proyecto
Código
Practico2-poo/
├── app.py              # Rutas principales Flask
├── models.py           # Modelos SQLAlchemy
├── templates/          # HTML con Jinja2
│   ├── base.html
│   ├── inicio.html
│   ├── login.html
│   ├── bandeja.html
│   └── asignacion.html
├── static/
│   └── css/
│       └── estilos.css
├── instance/           # Base de datos SQLite
├── requirements.txt    # Dependencias
└── .gitignore          # Archivos ignorados


👥 Autores:
- Gabriel Luna
- Julian Leal


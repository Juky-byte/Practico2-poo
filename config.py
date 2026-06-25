import os
from dotenv import load_dotenv

#Cargar variables de entorno desde .env
load_dotenv()

#Ruta base del proyecto (donde está config.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#Carpeta instance
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto")

    # URI absoluta de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(INSTANCE_DIR, "datos.sqlite3")
    )

    # Configuracion opcional (apagador de sensores internos)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carpeta de uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
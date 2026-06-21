import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # variables del entorno
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///datos.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configuracion para subida de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
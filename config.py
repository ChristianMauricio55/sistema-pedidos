import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta'

    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        database_url = database_url.replace("postgres://", "postgresql://")

        if "sslmode" not in database_url:
            database_url += "?sslmode=require"

    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///sistema_pedidos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
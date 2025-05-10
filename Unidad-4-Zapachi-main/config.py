import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-super-segura'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admi123@localhost/zapachi_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
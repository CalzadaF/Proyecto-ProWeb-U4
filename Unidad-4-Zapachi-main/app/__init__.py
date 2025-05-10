from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
gestor_login = LoginManager()
migrar = Migrate()

def crear_aplicacion(config_class=Config):
    app = Flask(__name__)
    app.config ['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://admin:$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW@localhost/zapachi_db')
    
    db.init_app(app)
    gestor_login.init_app(app)
    migrar.init_app(app, db)
    
    gestor_login.vista_login = 'autenticacion.iniciar_sesion'
    gestor_login.mensaje_categoria = 'info'
    
   
    from app.rutas.auth import auth_bp
    from app.rutas.admin import bp_administrador
    from app.rutas.productos import bp_productos
    from app.rutas.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_administrador, url_prefix='/admin')
    app.register_blueprint(bp_productos)
    app.register_blueprint(main_bp)
    
    return app
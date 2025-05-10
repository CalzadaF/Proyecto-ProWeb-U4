from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    """Factory principal para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Registrar Blueprints
    from app.rutas.main import main_bp
    from app.rutas.admin import admin_bp
    from app.rutas.productos import productos_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(productos_bp)

    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
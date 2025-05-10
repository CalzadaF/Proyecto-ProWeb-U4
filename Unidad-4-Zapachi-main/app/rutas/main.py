from flask import Blueprint, render_template
from flask_login import login_required
from app.modelos import Producto  # Asegúrate de importar tus modelos

# Configuración del Blueprint principal
main_bp = Blueprint('main', __name__)

#
@main_bp.route('/')
def index():
    productos_destacados = Producto.query.limit(4).all()
    return render_template('main/index.html', productos=productos_destacados)

@main_bp.route('/nosotros')
def nosotros():
    """Página 'Sobre nosotros'"""
    return render_template('main/nosotros.html')

@main_bp.route('/contacto')
def contacto():
    """Página de contacto"""
    return render_template('main/contacto.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Panel de control (requiere autenticación)"""
    return render_template('main/dashboard.html')

@main_bp.route('/catalogo')
def catalogo():
    """Página de catálogo de productos"""
    todos_productos = Producto.query.all()
    return render_template('main/catalogo.html', productos=todos_productos)

@main_bp.route('/producto/<int:id>')
def detalle_producto(id):
    """Detalle de un producto específico"""
    producto = Producto.query.get_or_404(id)
    return render_template('main/detalle_producto.html', producto=producto)
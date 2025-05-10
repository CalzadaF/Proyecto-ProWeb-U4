from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.modelos import Usuario, Producto, db
from app.formularios import FormularioProducto
from app.decoradores import administrador_requerido

admin_bp = Blueprint('administrador', __name__)

@admin_bp.route('/panel')
@login_required
@administrador_requerido
def panel():
    total_usuarios = Usuario.query.count()
    total_productos = Producto.query.count()
    return render_template('admin/panel.html', 
                         total_usuarios=total_usuarios,
                         total_productos=total_productos)

@admin_bp.route('/productos')
@login_required
@administrador_requerido
def gestionar_productos():
    productos = Producto.query.all()
    return render_template('admin/productos.html', productos=productos)

@admin_bp.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
@administrador_requerido
def agregar_producto():
    formulario = FormularioProducto()
    if formulario.validate_on_submit():
        producto = Producto(
            nombre=formulario.nombre.data,
            descripcion=formulario.descripcion.data,
            precio=formulario.precio.data,
            url_imagen=formulario.url_imagen.data,
            stock=formulario.stock.data,
            categoria=formulario.categoria.data
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado exitosamente', 'éxito')
        return redirect(url_for('administrador.gestionar_productos'))
    return render_template('admin/agregar_producto.html', formulario=formulario)
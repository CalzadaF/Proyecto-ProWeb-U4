from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required, current_user
from app.modelos import Producto, Pedido, ItemPedido, db
import json

productos_bp  = Blueprint('productos', __name__)

@productos_bp .route('/catalogo')
def catalogo():
    productos = Producto.query.all()
    return render_template('principal/catalogo.html', productos=productos)

@productos_bp .route('/carrito')
@login_required
def carrito():
    return render_template('main/catalogo.html', productos=productos)

@productos_bp .route('/api/carrito', methods=['GET', 'POST'])
@login_required
def manejar_carrito():
    if request.method == 'POST':
        datos = request.get_json()
        producto_id = datos.get('producto_id')
        cantidad = datos.get('cantidad', 1)
        talla = datos.get('talla', '')
        
        producto = Producto.query.get_or_404(producto_id)
        
        carrito = session.get('carrito', {})
        item_carrito = carrito.get(str(producto_id), {'cantidad': 0, 'talla': talla})
        item_carrito['cantidad'] += cantidad
        item_carrito['talla'] = talla
        carrito[str(producto_id)] = item_carrito
        session['carrito'] = carrito
        
        return jsonify({'exito': True, 'carrito': carrito})
    
    # GET request
    carrito = session.get('carrito', {})
    productos = []
    total = 0
    
    for producto_id, item in carrito.items():
        producto = Producto.query.get(producto_id)
        if producto:
            total_item = producto.precio * item['cantidad']
            total += total_item
            productos.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'url_imagen': producto.url_imagen,
                'cantidad': item['cantidad'],
                'talla': item['talla'],
                'total_item': total_item
            })
    
    return jsonify({'productos': productos, 'total': total})

@productos_bp .route('/api/finalizar-compra', methods=['POST'])
@login_required
def finalizar_compra():
    carrito = session.get('carrito', {})
    if not carrito:
        return jsonify({'exito': False, 'mensaje': 'El carrito está vacío'})
    
    try:
        pedido = Pedido(usuario_id=current_user.id, total=0)
        db.session.add(pedido)
        db.session.flush()  # Para obtener el ID del pedido
        
        total = 0
        for producto_id, item in carrito.items():
            producto = Producto.query.get(producto_id)
            if producto and producto.stock >= item['cantidad']:
                item_pedido = ItemPedido(
                    pedido_id=pedido.id,
                    producto_id=producto.id,
                    cantidad=item['cantidad'],
                    precio=producto.precio,
                    talla=item['talla']
                )
                db.session.add(item_pedido)
                producto.stock -= item['cantidad']
                total += producto.precio * item['cantidad']
        
        pedido.total = total
        db.session.commit()
        session.pop('carrito', None)
        return jsonify({'exito': True, 'pedido_id': pedido.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'exito': False, 'mensaje': str(e)})
    
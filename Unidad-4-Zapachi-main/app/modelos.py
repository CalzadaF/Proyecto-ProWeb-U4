from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime
from app.__init__ import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class Producto(db.Model):
    __tablename__ = 'productos'
    __table_args__ = {'extend_existing': True}  # Permite usar la tabla existente

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    url_imagen = db.Column(db.String(200))
    stock = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())
    actualizado_en = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def establecer_contraseña(self, contraseña):
        self.hash_contraseña = generate_password_hash(contraseña)
    
    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.hash_contraseña, contraseña)
    
    def es_administrador(self):
        return self.rol == 'administrador'
    
    def es_editor(self):
        return self.rol == 'editor'

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    url_imagen = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, server_default=db.func.now())
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, completado, cancelado
    creado_en = db.Column(db.DateTime, server_default=db.func.now())

class ItemPedido(db.Model):
    __tablename__ = 'items_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    talla = db.Column(db.String(10))
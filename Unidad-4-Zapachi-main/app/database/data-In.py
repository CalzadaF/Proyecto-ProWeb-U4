from app import crear_aplicacion
from app.modelos import db, Producto

app = crear_aplicacion()

with app.app_context():
    # Crear algunos productos iniciales
    productos_iniciales = [
        {
            "nombre": "Playera Hugo Boss",
            "descripcion": "Playera de alta calidad marca Hugo Boss",
            "precio": 1999.00,
            "url_imagen": "img/playera_hugo.jpg",
            "stock": 50,
            "categoria": "ropa"
        },
        {
            "nombre": "Tenis Yeezy",
            "descripcion": "Tenis deportivos Yeezy, edición limitada",
            "precio": 7899.00,
            "url_imagen": "img/yezy.jpg",
            "stock": 20,
            "categoria": "calzado"
        },
        {
            "nombre": "Gorra 3 pablos",
            "descripcion": "Gorra estilo urbano",
            "precio": 2499.00,
            "url_imagen": "img/3yos.jpeg",
            "stock": 30,
            "categoria": "accesorios"
        }
    ]
    
    for datos_producto in productos_iniciales:
        producto = Producto.query.filter_by(nombre=datos_producto['nombre']).first()
        if not producto:
            nuevo_producto = Producto(**datos_producto)
            db.session.add(nuevo_producto)
    
    db.session.commit()
    print("Productos iniciales creados exitosamente")
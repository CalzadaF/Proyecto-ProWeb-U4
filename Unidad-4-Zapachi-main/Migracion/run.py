from app import crear_aplicacion
import os

app = crear_aplicacion()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
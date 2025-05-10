from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app.modelos import Usuario, db
from app.formularios import FormularioLogin, FormularioRegistro

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if current_user.is_authenticated:
        return redirect(url_for('principal.index'))
    
    formulario = FormularioLogin()
    if formulario.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=formulario.correo.data).first()
        if usuario and check_password_hash(usuario.hash_contraseña, formulario.contraseña.data):
            login_user(usuario, remember=formulario.recordar.data)
            siguiente_pagina = request.args.get('next')
            return redirect(siguiente_pagina) if siguiente_pagina else redirect(url_for('principal.index'))
        flash('Correo o contraseña incorrectos', 'peligro')
    return render_template('auth/login.html', formulario=formulario)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('principal.index'))
    
    formulario = FormularioRegistro()
    if formulario.validate_on_submit():
        usuario = Usuario(
            nombre_usuario=formulario.nombre_usuario.data,
            correo=formulario.correo.data,
            rol='cliente'
        )
        usuario.establecer_contraseña(formulario.contraseña.data)
        db.session.add(usuario)
        db.session.commit()
        flash('¡Registro exitoso! Por favor inicia sesión.', 'éxito')
        return redirect(url_for('autenticacion.iniciar_sesion'))
    return render_template('auth/registro.html', formulario=formulario)

@auth_bp.route('/cerrar-sesion')
def cerrar_sesion():
    logout_user()
    return redirect(url_for('principal.index'))
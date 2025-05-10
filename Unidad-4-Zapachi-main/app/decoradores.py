from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def administrador_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_administrador():
            flash('Acceso no autorizado', 'peligro')
            return redirect(url_for('principal.index'))
        return f(*args, **kwargs)
    return funcion_decorada

def editor_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if not current_user.is_authenticated or (not current_user.es_editor() and not current_user.es_administrador()):
            flash('Acceso no autorizado', 'peligro')
            return redirect(url_for('principal.index'))
        return f(*args, **kwargs)
    return funcion_decorada
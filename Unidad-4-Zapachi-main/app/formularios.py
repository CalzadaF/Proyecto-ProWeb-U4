from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class FormularioLogin(FlaskForm):
    correo = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo es obligatorio'),
        Email(message='Ingrese un correo válido')
    ])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    recordar = BooleanField('Recordar sesión')
    enviar = SubmitField('Iniciar Sesión')

class FormularioRegistro(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=4, max=25, message='El nombre debe tener entre 4 y 25 caracteres')
    ])
    correo = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo es obligatorio'),
        Email(message='Ingrese un correo válido')
    ])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debe confirmar la contraseña'),
        EqualTo('contraseña', message='Las contraseñas no coinciden')
    ])
    enviar = SubmitField('Registrarse')

class FormularioProducto(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    url_imagen = StringField('URL de la Imagen', validators=[DataRequired(), Length(max=255)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    categoria = StringField('Categoría', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Agregar Producto')
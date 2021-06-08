from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField
from wtforms.validators import InputRequired, NumberRange, Length, Email
from flask_wtf.file import FileField, FileAllowed



class LoginForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Usuario",
        validators=[InputRequired()])
    password = PasswordField("Contraseña",
        validators=[InputRequired()])


class NewUserForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Usuario",
        validators=[InputRequired()])
    password = PasswordField("Contraseña",
        validators=[InputRequired()])
    email = StringField("Correo Electronico",
        validators=[InputRequired(), Email()])
    is_admin = RadioField("Administrador",
        choices=[(True, 'Si'), (False, 'No')],
        validators=[InputRequired()])


class ChangeMenuForm(FlaskForm):
    """Form for menu."""
    menu = TextAreaField("Menu",
        validators=[InputRequired(), Length(max=200, message='Maximo de 200 carácteres')])


class AddImageForm(FlaskForm):
    """Form for adding images."""

    photo_file = FileField("Añadir imagen",
        validators=[InputRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], 'Formato de imagen esta invalido.')])


class WhatsappPhoneForm(FlaskForm):
    """Form for whatsapp #."""
    whatsapp_phone = StringField("Numero de WhatsApp",
        validators=[InputRequired(), Length(min=10, max=14, message='Entra un numero entre 10 y 14 numeros')])


class ResetPasswordForm(FlaskForm):
    """Form for resetting password."""

    email = StringField("Correo Electronico",
        validators=[InputRequired(), Email()])

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
    isAdmin = RadioField("Administrador",
        validators=[InputRequired()])


class ChangeMenuForm(FlaskForm):
    """Form for menu."""
    menu = TextAreaField("Menu",
        validators=[InputRequired(), Length(max=200)])


class AddImageForm(FlaskForm):
    """Form for adding images."""

    photo_file = FileField("Añadir imagen",
        validators=[InputRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], 'Formato de imagen esta invalido.')])

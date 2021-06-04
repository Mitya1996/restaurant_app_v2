from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, Length, Email



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
    email = PasswordField("Correo Electronico",
        validators=[InputRequired(), Email()])
    isAdmin = PasswordField("Contraseña",
        validators=[InputRequired()])


class ChangeMenuForm(FlaskForm):
    """Form for menu."""
    menu = TextAreaField("Menu",
        validators=[InputRequired(), Length(max=200)])



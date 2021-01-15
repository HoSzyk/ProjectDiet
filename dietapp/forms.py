from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[validators.Length(min=3, max=25),
                                                            validators.DataRequired(
                                                                message="Proszę uzupełnić pole email!")])
    password = PasswordField("Hasło", validators=[validators.DataRequired(message="Nie podałeś hasła!")])

    remember = BooleanField("Zapamiętaj mnie!")

    submit = SubmitField("Zaloguj się")

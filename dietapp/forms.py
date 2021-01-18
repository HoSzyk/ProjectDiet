from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, Form
from wtforms.validators import ValidationError
from dietapp.models import User


class LoginForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[validators.Length(min=3, max=25),
                                                            validators.DataRequired(
                                                                message="Proszę uzupełnić pole email!")])
    password = PasswordField("Hasło", validators=[validators.DataRequired(message="Nie podałeś hasła!")])

    remember = BooleanField("Zapamiętaj mnie!")

    submit = SubmitField("")


class RegisterForm(FlaskForm):
    name = StringField("Nazwa profilu", validators=[validators.DataRequired("Wprowadź nazwę")])

    email = StringField("Email", validators=[validators.Email(message="Prosze wprowadzić poprawny adres email")])

    password = PasswordField("Hasło", validators=[
        validators.DataRequired(message="Proszę wprowadzić hasło dla konta"),
        validators.equal_to(fieldname="confirm_password", message="Twoje hasła muszą się zgadzać")
    ])

    confirm_password = PasswordField("Potwierdź hasło",
                                     validators=[validators.DataRequired(message="Proszę potwierdzić hasło")])

    submit = SubmitField("")

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Użytkownik o takiej nazwie już istnieje. Proszę wybrać inną nazwę.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email jest już w użyciu. Proszę wybrać inny.')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.posts.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        if not username.data:
            return

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username вже зайнятий.')

    def validate_email(self, email):
        if not email.data:
            return

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email вже зареєстрований.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запам’ятати мене')
    submit = SubmitField('Увійти')
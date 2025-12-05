from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    """Форма для контактів згідно з вимогами."""
    
    
    name = StringField('Ім\'я', validators=[
        DataRequired(),
        Length(min=4, max=10, message="Ім'я має бути від 4 до 10 символів")
    ])
    
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Некоректний формат email")
    ])
    
    
    phone = StringField('Телефон', validators=[
        DataRequired(),
        Regexp(r'^\+380\d{9}$', message="Телефон має бути у форматі +380XXXXXXXXX")
    ])
    
    
    subject = SelectField('Тема', choices=[
        ('tech_support', 'Технічна підтримка'),
        ('sales', 'Відділ продажів'),
        ('general', 'Загальне питання')
    ], validators=[DataRequired()])
    
    
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(),
        Length(max=500, message="Повідомлення не може перевищувати 500 символів")
    ])
    
    submit = SubmitField('Відправити')



class LoginForm(FlaskForm):
    """Форма для логіну згідно з вимогами."""
    
    
    username = StringField('Ім\'я користувача (або Email)', validators=[
        DataRequired(message="Це поле є обов'язковим")
    ])
    
    
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ])
    
    
    remember = BooleanField("Запам'ятати мене")
    
    submit = SubmitField('Увійти')
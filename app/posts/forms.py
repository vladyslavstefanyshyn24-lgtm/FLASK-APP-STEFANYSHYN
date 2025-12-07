from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from .models import Category

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Контент', validators=[DataRequired()])
    category = SelectField('Категорія', 
                           choices=[(c.value, c.value.capitalize()) for c in Category],
                           validators=[DataRequired()])
    is_active = BooleanField('Активний', default=True)
    posted = DateTimeLocalField('Дата та час', format='%Y-%m-%dT%H:%M', default=datetime.utcnow)
    submit = SubmitField('Зберегти')
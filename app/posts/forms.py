from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateTimeLocalField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from .models import Category, User, Tag


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Контент', validators=[DataRequired()])
    category = SelectField('Категорія',
                           choices=[(c.value, c.value.capitalize()) for c in Category],
                           validators=[DataRequired()])
    is_active = BooleanField('Активний', default=True)
    posted = DateTimeLocalField('Дата та час', format='%Y-%m-%dT%H:%M', default=datetime.utcnow)

    author_id = SelectField('Автор', coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField('Теги', coerce=int)

    submit = SubmitField('Зберегти')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id.choices = [(u.id, u.username) for u in User.query.order_by(User.username).all() or []]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all() or []]
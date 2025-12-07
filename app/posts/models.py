from app import db
from datetime import datetime
from enum import Enum as PyEnum

class Category(PyEnum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.Enum(Category), default=Category.other)
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default='Anonymous')

    def __repr__(self):
        return f'<Post {self.title[:30]}...>'

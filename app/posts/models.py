from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, String, Text, DateTime, Boolean, ForeignKey,
    Table, Column, text
)
from sqlalchemy.types import Enum as SQLEnum
from datetime import datetime
from typing import List
import enum


class Category(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'


post_tags = Table(
    'post_tags',
    db.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


# ------------------- Tag -------------------
class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", secondary=post_tags, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


# ------------------- User -------------------
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"
    def is_active(self):
            return True
    def is_authenticated(self):
            return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)
        
# ------------------- Post -------------------
class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    category: Mapped[Category] = mapped_column(
        SQLEnum(Category), default=Category.other, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="posts")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=post_tags, back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.title[:30]}...>"
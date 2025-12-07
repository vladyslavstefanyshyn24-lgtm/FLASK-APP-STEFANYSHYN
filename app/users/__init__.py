# app/users/__init__.py
from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Імпортуємо роути ПОТІМ, щоб уникнути circular imports
from . import views   # або routes.py, залежно як у тебе називається файл
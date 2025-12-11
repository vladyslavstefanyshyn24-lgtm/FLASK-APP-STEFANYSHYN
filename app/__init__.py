from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

load_dotenv()

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.posts import post_bp
    from app.products import products_bp
    app.register_blueprint(post_bp)
    app.register_blueprint(products_bp)

    from app.users import users_bp
    app.register_blueprint(users_bp)

    @app.route('/')
    def home():
        return redirect(url_for('posts.list_posts'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from app.posts import models
        from app.products import models

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.posts.models import User
    return User.query.get(int(user_id))
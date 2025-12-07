from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.posts import post_bp
    app.register_blueprint(post_bp)

    @app.route('/')
    def home():
        return redirect(url_for('posts.index'))

    with app.app_context():
        from app.posts import models
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    return app

from flask import Flask
from loguru import logger

 
app = Flask(__name__)


app.config.from_pyfile('../config.py')


logger.add("logs/contact_form.log", rotation="10 MB", retention="1 month", level="INFO", 
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


from app.users.views import users_bp
app.register_blueprint(users_bp)


from app import views
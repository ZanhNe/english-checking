from app.extentions.extentions import cors, security, mail, migrate
from app.controllers.writing import writing_view
from app.controllers.home import home_view
from app.controllers.reading import reading_view
from app.controllers.speaking import speaking_view
from app.controllers.listening import listening_view
from app.models.models import db
from app.admin.admin import admin
from config import Config
from flask import Flask



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(obj=Config)
    db.init_app(app=app)
    cors.init_app(app=app)
    security.init_app(app=app)
    migrate.init_app(app=app)
    mail.init_app(app=app)
    admin.init_app(app=app)
    app.register_blueprint(blueprint=home_view)
    app.register_blueprint(blueprint=writing_view)
    app.register_blueprint(blueprint=reading_view)
    app.register_blueprint(blueprint=speaking_view)
    app.register_blueprint(blueprint=listening_view)
    return app




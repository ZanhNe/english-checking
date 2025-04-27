from app.extentions.extentions import cors
from app.controllers.writing import writing_view
from app.controllers.home import home_view
from app.controllers.reading import reading_view
from app.controllers.listening import listening_view
from config import Config
from flask import Flask



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(obj=Config)
    cors.init_app(app=app)
    app.register_blueprint(blueprint=home_view)
    app.register_blueprint(blueprint=writing_view)
    app.register_blueprint(blueprint=reading_view)
    app.register_blueprint(blueprint=listening_view)
    return app




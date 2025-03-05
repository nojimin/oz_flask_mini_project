from config import db
from flask import Flask
from flask_migrate import Migrate
from app.routes import image_bp, api, question_choices_bp
import app.models

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)

    # 이어서 블루 프린트 등록 코드를 작성해주세요!
    
    application.register_blueprint(api, url_prefix="/api")
    application.register_blueprint(image_bp, url_prefix="/images")
    application.register_blueprint(question_choices_bp, url_prefix="/questions")

    return application

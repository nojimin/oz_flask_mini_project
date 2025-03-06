from config import db
from flask import Flask
from flask_migrate import Migrate
from app.routes import main_bp, image_bp, questions_bp, choice_bp


migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    with application.app_context():
        import app.models  # 모델을 명확히 로드하여 Flask-Migrate가 인식 가능하도록 함.


    migrate.init_app(application, db)

    # 이어서 블루 프린트 등록 코드를 작성해주세요!
    
    application.register_blueprint(main_bp)
    application.register_blueprint(image_bp, url_prefix="/images")
    application.register_blueprint(questions_bp, url_prefix="/questions")
    application.register_blueprint(choice_bp, url_prefix="/choice")

    return application

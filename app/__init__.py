from config import db
from flask import Flask
from flask_migrate import Migrate

import app.models

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)

    # 이어서 블루 프린트 등록 코드를 작성해주세요!

    return application

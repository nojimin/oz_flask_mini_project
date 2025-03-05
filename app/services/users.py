from config import db
from app.models import User
from flask import abort

# 유저 생성
def create_user(name, age, gender, email):
    try:
        # 유저를 데이터베이스에 저장
        user = User(name=name, age=age, gender=gender, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        abort(400, f"유저 생성 중 오류 발생: {str(e)}")

# 유저 전체 조회
def get_all_users():
    return User.query.all()

# 유저 단일 조회 (ID로 조회)
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, "유저를 찾을 수 없습니다")
    return user

# 유저 단일 조회 (이메일로 조회)
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(404, "유저를 찾을 수 없습니다")
    return user

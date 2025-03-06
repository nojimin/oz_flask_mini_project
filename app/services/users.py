from config import db
from app.models import User
from flask import abort

# 유저 생성
def create_user(name, email, age, gender):
    try:
        # 유저 객체 생성
        user = User(name=name, email=email, age=age, gender=gender)
        db.session.add(user)
        db.session.commit()  # DB 커밋
        return user
    except Exception as e:
        db.session.rollback()  # 예외 발생 시 롤백
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
    if user:
        return user  # 이미 유저가 존재하면 해당 유저 객체 반환
    return None  # 유저가 없으면 None 반환


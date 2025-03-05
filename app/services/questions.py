# question.py
from config import db
from models import Question, Image
from flask import abort

# 질문 생성
def create_question(title, image_id, is_active=True, sqe=None):
    # 이미지가 존재하는지 확인
    image = Image.query.get(image_id)
    if not image:
        abort(400, '이미지가 존재하지 않습니다')

    # 질문을 데이터베이스에 저장
    question = Question(title=title, image_id=image_id, is_active=is_active, sqe=sqe)
    db.session.add(question)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        abort(500, message=f"질문 생성 중 오류 발생: {str(e)}")
        
    return question

# 질문 전체 조회
def get_all_questions():
    return Question.query.all()

# 질문 단일 조회
def get_question_by_id(question_id):
    return Question.query.get(question_id)
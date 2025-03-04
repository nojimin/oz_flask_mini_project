from config import db
from models import Choices, Question
from flask import abort

# 선택지 생성
def create_choice(question_id, content, is_active=True, sqe=None):
    # 질문이 존재하는지 확인
    question = Question.query.get(question_id)
    if not question:
        abort(404, '질문을 찾을 수 없습니다')

    # 선택지를 데이터베이스에 저장
    choice = Choices(content=content, is_active=is_active, sqe=sqe, question_id=question_id)
    db.session.add(choice)
    db.session.commit()
    return choice

# 선택지 전체 조회
def get_choices_by_question_id(question_id):
    return Choices.query.filter(Choices.question_id == question_id).all()

# 선택지 단일 조회
def get_choice_by_id(choice_id):
    return Choices.query.filter(Choices.id == choice_id).first()
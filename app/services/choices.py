# choices.py
from config import db
from app.models import Choices, Question
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

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        abort(500, message=f"선택지 생성 중 오류 발생: {str(e)}")

    return choice

# 선택지 전체 조회
def get_choices_by_question_id(question_id):
    choices = Choices.query.filter(Choices.question_id == question_id).all()
    # 선택지가 없으면 404 예외 발생
    if not choices:
        abort(404, '해당 질문에 대한 선택지가 없습니다')
    return choices

# 선택지 단일 조회
def get_choice_by_id(choice_id):
    choice = Choices.query.get(choice_id)
    if not choice:
        abort(404, description="해당 선택지가 존재하지 않습니다.")
    return choice
from config import db
from models import Answer, User, Choices
from flask import abort

# 답변 생성
def create_answer(user_id, choice_id):
    # 유저와 선택지가 존재하는지 확인
    user = User.query.get(user_id)
    if not user:
        abort(404, '유저를 찾을 수 없습니다')

    choice = Choices.query.get(choice_id)
    if not choice:
        abort(404, '선택지를 찾을 수 없습니다')

    # 답변을 데이터베이스에 저장
    answer = Answer(user_id=user_id, choice_id=choice_id)
    db.session.add(answer)
    db.session.commit()
    return answer.to_dict()

# 특정 유저의 모든 답변 조회
def get_answers_by_user_id(user_id):
    return Answer.query.filter_by(user_id=user_id).all()

# 특정 선택지에 대한 모든 답변 조회
def get_answers_by_choice_id(choice_id):
    return Answer.query.filter_by(choice_id=choice_id).all()

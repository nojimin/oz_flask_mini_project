# routes.py
from flask import Blueprint, request, jsonify
from config import db
from models import Question, Choices, Image
from services import create_question, get_question_by_id, get_all_questions, create_choice, get_choices_by_question_id
from flask_smorest import abort

# Blueprint 생성
bp = Blueprint('api', __name__)

# 4.1 특정 질문 가져오기
@bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = get_question_by_id(question_id)
    choices = get_choices_by_question_id(question_id)

    # 질문이 있는지 확인
    if not question:
        abort(404, message="질문을 찾을 수 없습니다.")

    # 질문에 연결된 이미지 가져오기
    image_url = None
    if question.image_id:
        image = Image.query.get(question.image_id)
        image_url = image.url if image else None

    return jsonify({
        "id": question.id,
        "title": question.title,
        "image": image_url,
        "choices": [
            {"id": choice.id, "content": choice.content, "is_active": choice.is_active}
            for choice in choices
        ]
    })

# 4.2 질문 개수 확인
@bp.route('/questions/count', methods=['GET'])
def get_question_count():
    count = Question.query.count()
    return jsonify({"total": count})

# 5. 특정 질문의 선택지 가져오기
@bp.route('/choice/<int:question_id>', methods=['GET'])
def get_choices(question_id):
    choices = get_choices_by_question_id(question_id)

    return jsonify({
        "choices": [
            {"id": choice.id, "content": choice.content, "is_active": choice.is_active}
            for choice in choices
        ]
    })

# 7.2 질문 생성
@bp.route('/question', methods=['POST'])
def add_question():
    data = request.get_json()
    title = data.get('title')
    image_id = data.get('image_id')
    is_active = data.get('is_active', True)
    sqe = data.get('sqe')

    if not title:
        abort(400, message="질문 제목은 필수입니다.")

    try:
        question = create_question(title, image_id, is_active, sqe)
        return jsonify({"message": f"Title: {question.title} question Success Create"})
    except Exception as e:
        abort(500, message=f"질문 생성 중 오류 발생: {str(e)}")

# 7.3 선택지 생성
@bp.route('/choice', methods=['POST'])
def add_choice():
    data = request.get_json()
    question_id = data.get('question_id')
    content = data.get('content')
    is_active = data.get('is_active', True)
    sqe = data.get('sqe')

    if not question_id or not content:
        abort(400, message="question_id와 content는 필수입니다.")

    try:
        choice = create_choice(question_id, content, is_active, sqe)
        return jsonify({"message": f"Content: {choice.content} choice Success Create"})
    except Exception as e:
        abort(500, message=f"선택지 생성 중 오류 발생: {str(e)}")
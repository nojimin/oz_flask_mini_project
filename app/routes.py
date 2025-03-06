# routes.py
from flask import Flask, Blueprint, request, jsonify, abort
from flask_smorest import abort
from app.models import Question, Choices, Image, User, Answer
from config import db
from app.services.users import create_user, get_user_by_id, get_user_by_email
from app.services.answers import create_answer
from app.services.questions import create_question, get_question_by_id, get_all_questions
from app.services.choices import create_choice, get_choices_by_question_id, get_choice_by_id
from app.services.images import upload_image, load_image

# Buleprint
main_bp = Blueprint('main', __name__)
image_bp = Blueprint('images', __name__)
questions_bp = Blueprint('questions_bp', __name__)
choice_bp = Blueprint('choice', __name__)

# 1. 기본 연결 확인
@main_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Success Connect"}), 200

# 2. 메인 이미지 가져오기
@image_bp.route('/main', methods=['GET'])
def get_main_image():
    try:
        print("메인 이미지 조회 시작")
        # 'main' 타입의 이미지를 검색
        main_image = Image.query.filter_by(image_type='main').first()

        if not main_image:
            abort(404, description="메인 이미지를 찾을 수 없습니다.")
        
        print(f"메인 이미지 URL: {main_image.url}")

        # 응답 데이터 반환
        return jsonify({
            "image": main_image.url
        })

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        # 예기치 않은 오류 발생 시 500 에러 반환
        return jsonify({"message": f"서버 오류 발생: {str(e)}"}), 500

# 3. 회원가입
@main_bp.route("/signup", methods=["POST"])
def signup():
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")
    data = request.get_json()
    required_fields = {"name", "email", "age", "gender"}

    if not required_fields.issubset(data):
        abort(400, "필수 입력값(name, email, age, gender)이 누락되었습니다.")

    # 이메일 중복 확인
    existing_user = get_user_by_email(data["email"])
    if existing_user:
        return jsonify({"message": "이미 존재하는 계정 입니다."}), 400  # 이메일이 이미 존재함

    user = create_user(data["name"], data["email"], data["age"], data["gender"])
    return jsonify({
        "message": f"{user.name}님 회원가입을 축하합니다",
        "user_id": user.id
    }), 200

# 4.1 질문 가져오기
@questions_bp.route('/<int:question_id>', methods=['GET'])
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
@questions_bp.route('/count', methods=['GET'])
def get_question_count():
    count = Question.query.count()
    return jsonify({"total": count})

# 5. 선택지 가져오기
@choice_bp.route('/<int:question_id>', methods=['GET'])
def get_choices(question_id):
    choices = get_choices_by_question_id(question_id)

    return jsonify({
        "choices": [
            {"id": choice.id, "content": choice.content, "is_active": choice.is_active}
            for choice in choices
        ]
    })

# 6. 답변 제출하기
@main_bp.route("/submit", methods=["POST"])
def submit_answers():
    data = request.get_json()
    print(data)  # 요청 데이터를 확인
    if not isinstance(data, list):
        abort(400, description="요청 데이터는 리스트 형태여야 합니다.")

    user_id = None
    answers = []

    for item in data:
        if "user_id" not in item or "choice_id" not in item:
            abort(400, description="user_id와 choice_id는 필수 입력값입니다.")

        # 첫 번째 user_id를 기준으로 검증
        if user_id is None:
            user_id = item["user_id"]
        elif user_id != item["user_id"]:
            abort(400, description="모든 답변은 동일한 user_id를 가져야 합니다.")

        # 해당 유저가 존재하는지 확인
        user = get_user_by_id(item["user_id"])
        if not user:
            abort(404, description="해당 유저가 존재하지 않습니다.")

        # 해당 선택지가 존재하는지 확인
        choice = get_choice_by_id(item["choice_id"])  # 수정된 부분
        if not choice:
            abort(404, description="해당 선택지가 존재하지 않습니다.")

        # 답변 저장
        try:
            answer = create_answer(item["user_id"], item["choice_id"])
            answers.append(answer)
        except Exception as e:
            abort(500, description=f"답변 저장 중 오류 발생: {str(e)}")

    return jsonify({
        "message": f"User: {user_id}'s answers Success Create"
    }), 200

# 7.1 이미지 생성
@image_bp.route('', methods=['POST'])
def handle_images():
    data = request.get_json()

    if not data or 'url' not in data or 'type' not in data:
        abort(400, description="이미지 URL과 타입이 필요합니다.")

    url = data['url']
    image_type = data['type']

    # image_type이 올바른 값인지 확인
    if image_type not in ['main', 'sub']:
        abort(400, description="잘못된 이미지 타입입니다. 'main' 또는 'sub'만 가능합니다.")

    # 이미지 추가
    new_image = Image(url=url, image_type=image_type)  # image_type을 올바르게 전달
    db.session.add(new_image)
    db.session.commit()

    return jsonify({
        "message": f"ID: {new_image.id} Image Success Create"
    }), 201

# 7.2 질문 생성
@main_bp.route('/question', methods=['POST'])
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
@choice_bp.route('', methods=['POST'])
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



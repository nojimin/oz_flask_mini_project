from flask import Blueprint, request, jsonify, abort
from flask_smorest import Api
from app.services.users import create_user, get_user_by_id, get_user_by_email, get_choice_by_id, create_answer
from app.services.answers import submit_answers

api = Blueprint("api", __name__)
swagger = Api(api)  # Swagger-UI 설정

# 기본 연결 확인
@api.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Success Connect"}), 200


# 회원가입
@api.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    required_fields = {"name", "email", "age", "gender"}

    if not required_fields.issubset(data):
        abort(400, "필수 입력값(name, email, age, gender)이 누락되었습니다.")

    # 이메일 중복 확인
    if get_user_by_email(data["email"]):  
        return jsonify({"message": "이미 존재하는 계정 입니다."}), 400

    user = create_user(data["name"], data["email"], data["age"], data["gender"])
    return jsonify({
        "message": f"{user.name}님 회원가입을 축하합니다",
        "user_id": user.id
    }), 200  # ← 201에서 200으로 변경

# 답변 제출하기
@api.route("/submit", methods=["POST"])
def submit_answers():
    data = request.get_json()

    if not isinstance(data, list):
        abort(400, "요청 데이터는 리스트 형태여야 합니다.")

    user_id = None
    answers = []

    for item in data:
        if "user_id" not in item or "choice_id" not in item:
            abort(400, "user_id와 choice_id는 필수 입력값입니다.")

        # 첫 번째 user_id를 기준으로 검증
        if user_id is None:
            user_id = item["user_id"]
        elif user_id != item["user_id"]:
            abort(400, "모든 답변은 동일한 user_id를 가져야 합니다.")

        # 해당 유저가 존재하는지 확인
        if not get_user_by_id(item["user_id"]):
            abort(404, "해당 유저가 존재하지 않습니다.")

        # 해당 선택지가 존재하는지 확인
        if not get_choice_by_id(item["choice_id"]):
            abort(404, "해당 선택지가 존재하지 않습니다.")

        # 답변 저장
        answer = create_answer(item["user_id"], item["choice_id"])
        answers.append(answer)

    return jsonify({
        "message": f"User: {user_id}'s answers Success Create"
    }), 200


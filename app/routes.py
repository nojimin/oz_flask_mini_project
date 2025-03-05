from flask import Blueprint, request, jsonify, abort
from app.services.images import upload_image, load_image

image_bp = Blueprint('images', __name__)

@image_bp.route('', methods=['GET', 'POST'])
def handle_images():
    if request.method == 'GET':
        image_id = request.args.get('id', type=int)
        if image_id:
            image = load_image(image_id)
            return jsonify({
                "id": image.id,
                "url": image.url,
                "description": image.description
            })
        else:
            abort(400, description="이미지 ID가 필요합니다.")

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'url' not in data:
            abort(400, description="이미지 URL이 필요합니다.")
        
        url = data['url']
        description = data.get('description', '')
        new_image = upload_image(url, description)
        
        return jsonify({
            "message": "이미지가 성공적으로 업로드되었습니다.",
            "id": new_image.id,
            "url": new_image.url,
            "description": new_image.description
        }), 201

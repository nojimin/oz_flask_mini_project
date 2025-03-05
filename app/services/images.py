from app import db
from app.models import Image
from flask import abort

# db에 새로운 이미지 저장
# url: 이미지 URL, image_type: 이미지 타입
def upload_image(url, image_type):
    # image_type이 main 또는 sub인지 확인
    if image_type not in ['main', 'sub']:
        abort(400, description="Invalid image type. Allowed values: 'main', 'sub'.")

    image = Image(url=url, image_type=image_type)  # image_type을 올바르게 전달
    db.session.add(image)
    db.session.commit()
    return image

# 주어진 id로 이미지 조회
def load_image(image_id):
    image = Image.query.get(image_id)
    # ERROR : image-id를 찾을 수 없으면 404 에러 발생
    if image is None:
        abort(404, description="이미지를 찾을 수 없습니다.")
    
    return image

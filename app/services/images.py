from app import db
from app.models import Image
from flask import abort

#db에 새로운 이지미 저장
# url: 이미지 URL, descriotion: 설명
def upload_image(url, descriotion=''):
    image = Image(url=url, descriotion=descriotion)
    db.session.add(image)
    db.session.commit()
    return image

# 주어진 id로 이미지 조회
def load_image(image_id):

    image =  Image.query.get(image_id)
    # ERROR : image-id를 찾을수 없으면 404에러 발생
    if image is None:
        abort(404, description = "이미지를 찾을 수 없습니다.")
        
    return image

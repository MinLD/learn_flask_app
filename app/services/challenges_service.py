from ..extensions import db
from .organization_service import user_get_organization_by_id
from .users_service import get_user_by_id
from ..models.models_model import Challenge
from ..services.upload_service import upload_file

def get_challenge_by_id(challenge_id):
    return Challenge.query.filter_by(id=challenge_id).first()

def create_challenge(data, current_user_id, organization_id=None, user_id=None):
    if not data:
        return None, "Thiếu thông tin bắt buộc"

    creator_user = None
    creator_org = None

    if organization_id:
        organization, error = user_get_organization_by_id(organization_id, current_user_id)
        if error:
            return None, error 
        creator_org = organization

    elif user_id:
        if user_id != current_user_id:
            return None, "Không có quyền tạo thử thách cho người dùng khác"
        user = get_user_by_id(user_id)
        if not user:
            return None, "Không tìm thấy người dùng"
        creator_user = user
    
    else:
        return None, "Phải chỉ định người tạo thử thách (user hoặc organization)"

    name = data.get('name')
    description = data.get('description')
    location = data.get('location')
    images = data.get('images', [])

    if not all([name, description, location, images]):
        return None, "Thiếu thông tin bắt buộc của thử thách (name, description, location, images)"
    
    new_challenge = Challenge(
        name= name, 
        description=description,
        location=location,
    )
    
    if creator_org:
        new_challenge.organization = creator_org
    elif creator_user:
        new_challenge.user = creator_user

    images_upload = []
    for file in data['images']:
        media_object = upload_file(file, current_user_id)
        images_upload.append(media_object)
    new_challenge.images = images_upload
    
    db.session.add(new_challenge)
    db.session.commit()
    return new_challenge, None

def get_all_challenges_idea(page, per_page):
    return Challenge.query.filter_by(status='idea').paginate(page=page, per_page=per_page)

#admin
def active_challenge(challenge_id):
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        return None, "Không tìm thấy thử thách"
    challenge.status = 'idea'
    db.session.commit()
    return "Kiểm duyệt thử thách thành công", None

def reject_challenge(challenge_id):
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        return None, "Không tìm thấy thử thách"
    challenge.status = 'rejected'
    db.session.commit()
    return "Từ chối thử thách thành công", None

def get_all_challenges_pending  (page, per_page):
    return Challenge.query.filter_by(status='pending').paginate(page=page, per_page=per_page)
   



 
    
        
    

        
        


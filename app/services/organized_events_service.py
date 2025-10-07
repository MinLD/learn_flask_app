from ..models.models_model import Organized_Events, User
from ..extensions import db
from ..services.users_service import get_user_by_id
from ..services.organization_service import get_organization_by_id
from ..services.challenges_service import get_challenge_by_id

def get_organized_event_by_id(organized_event_id):
    return Organized_Events.query.filter_by(id=organized_event_id).first()

def create_organized_event(data):
    if not data:
        return None, "Thiếu thông tin bắt buộc"
    organization_id = data.get('organization_id')
    organization = get_organization_by_id(organization_id=organization_id)
    if not organization:
        return None, "Không tìm thấy doanh nghiệp"
    challenge_id = data.get('challenge_id _id')
    print(f"ĐANG TÌM KIẾM CHALLENGE VỚI ID: {challenge_id}, KIỂU DỮ LIỆU: {type(challenge_id)}")
    challenge = get_challenge_by_id(challenge_id=challenge_id)
    if not challenge:
        return None, "Không tìm thấy thử thách"
    end_date = data.get('end_date')

    new_organized_event = Organized_Events(organization_id=organization_id, end_time=end_date, challenge_id= challenge_id)
    db.session.add(new_organized_event)
    db.session.commit()
    return new_organized_event, None

def join_organized_event(organized_event_id, user_id):
    organized_event = get_organized_event_by_id(organized_event_id)
    if not organized_event:
        return None, "Không tìm thấy sự kiện doanh nghiệp"
    user = get_user_by_id(user_id)
    if not user:
        return None, "Không tìm thấy người dùng"
    organized_event.participants.append(user)
    db.session.commit()
    return "Tham gia sự kiện doanh nghiệp thành công", None

def get_all_organized_events_approved():
    return Organized_Events.query.filter_by(status='approved').all()

    

    
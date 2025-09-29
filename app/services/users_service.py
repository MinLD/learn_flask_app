
from ..models.models_model import User, UserProfile
from ..extensions import db
from .role_service import get_role_by_name
from ..schemas.users_schemas import UserSchema



def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()
    

def get_email_profile(email):
    return UserProfile.query.filter_by(email=email).first()

def save(data):
    db.session.add(data)
    db.session.commit()
    
def delete(data):
    db.session.delete(data)
    db.session.commit()

def model_register(data ):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = get_role_by_name(name='user')
        if not username or not password or not email:
            return None, "Thiếu thông tin bắt buộc hoặc thông tin rỗng (username, password, email)"
        if get_user_by_username(username):
            return None, "Tên đăng nhập đã tồn tại"
        if get_email_profile(email):
            return None, "Email đã tồn tại"
        
        new_profile = UserProfile(email=email, avatar=None, fullname=None, bio=None, date_of_birth=None)
        new_user = User(username=username,roles=[role], profile=new_profile)
   
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return new_user, None

def update_user_profile(data, user_id):
    user = get_user_by_id(user_id)
    if not user:
        return None, "Không tìm thấy người dùng"
    if not data:
        return None, "Thiếu thông tin bắt buộc"

    if 'email' in data:
        user.profile.email = data.get('email')
    if 'avatar' in data:
        user.profile.avatar = data.get('avatar')
    if 'fullname' in data:
        user.profile.fullname = data.get('fullname')
    if 'bio' in data:
        user.profile.bio = data.get('bio')
    if 'date_of_birth' in data:
        user.profile.date_of_birth = data.get('date_of_birth')

        db.session.commit()
        return user, None

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return None, "Không tìm thấy người dùng"
    db.session.delete(user)
    db.session.commit()
    return "Xóa người dùng thành công", None
def get_all_users (page , per_page):
    users = User.query.paginate(page=page, per_page=per_page)
    return  UserSchema().dump(users, many=True)
   
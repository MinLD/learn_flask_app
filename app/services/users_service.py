
from ..models.models_model import User
from ..extensions import db
from .role_service import get_role_by_name
from ..schemas.users_schemas import UserSchema



def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
    
def get_user_by_email(email):
    return User.query.filter_by(email=email).first() 

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
        if get_user_by_email(email):
            return None, "Email đã tồn tại"
        
        
        new_user = User(username=username, email=email, roles=[role])
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return new_user, None
def get_all_users (page , per_page):
    users = User.query.paginate(page=page, per_page=per_page)
    return  UserSchema().dump(users, many=True)
   
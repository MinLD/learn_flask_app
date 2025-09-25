from .auth_model import User
from ..schemas.users_schemas import UserSchema


def get_all_users (page , per_page):
    users = User.query.paginate(page=page, per_page=per_page)
    return  UserSchema().dump(users, many=True)
   

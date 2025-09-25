from flask import Blueprint
from ..models.users_model import get_all_users
from ..utils.response import success_response
from flask import request
from ..schemas.users_schemas import UserSchema
from ..models.users_model import User
from flask_jwt_extended import jwt_required
from .auth_controller import admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@admin_required()
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return success_response(get_all_users(page, per_page), code=200)




   


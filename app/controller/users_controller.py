from flask import Blueprint
from ..utils.response import success_response, error_response
from flask import request
from .auth_controller import Role_required
from ..services.users_service import model_register, get_all_users

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@Role_required(role='admin')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return success_response(get_all_users(page, per_page), code=200)

@users_bp.route('/register', methods=['POST'])
def register(): 
    data = request.get_json()
    
    if not data:
        return error_response('Request body phải là JSON hoặc bị thiếu', 400)

    user, error = model_register( data)

    if error:
        status_code = 409 if "tồn tại" in error else 400
        return error_response(error, status_code)

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar if user.avatar else None,
        'is_active': user.is_active ,
        'created_at': user.created_at
    }
    
    return success_response(user_data, code=201)




   


from flask import Blueprint
from ..utils.response import success_response, error_response
from flask import request
from .auth_controller import Role_required
from ..services.users_service import model_register, get_all_users,update_user_profile, delete_user , get_user_by_id, update_password
from ..schemas.users_schemas import UserSchema
from flask_jwt_extended import jwt_required
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

    user_data = UserSchema().dump(user)
    
    return success_response(user_data, code=201)

@users_bp.route('/<string:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    data = request.form.to_dict()
    if 'avatar' in request.files:
        data['avatar'] = request.files['avatar']
    updated_user, error = update_user_profile(data, user_id)



    if error:
        return error_response(error, 400)
    
    return success_response(UserSchema().dump(updated_user), code=200)

@users_bp.route('/<string:user_id>', methods=['DELETE'])
@Role_required(role='admin')
def controller_delete_user(user_id):
    user, error = delete_user(user_id)
    if error:
        return error_response(error, 400)
    return success_response(user, code=200)

@users_bp.route('/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return error_response("Không tìm thấy người dùng", 404)
    return success_response(UserSchema().dump(user), code=200)

@users_bp.route('/password/<string:user_id>', methods=['PATCH'])
@jwt_required()
def update_password_user(user_id):
    data = request.get_json()
    error = update_password(user_id, data)
    if error:
        return error_response(error, 400)
    return success_response("Đổi mật khẩu người dùng thành công", code=200)


   


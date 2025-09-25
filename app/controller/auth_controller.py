from flask import Blueprint, request, jsonify
from ..models.auth_model import User
from ..utils.response import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
auth_bp = Blueprint('auth_bp', __name__)
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()  
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if "admin" in claims.get("roles", []):
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Admin access required!"}), 403
        return decorator
    return wrapper
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return error_response('Request body phải là JSON hoặc bị thiếu', 400)

    user, error = User.model_register(data)

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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return error_response('Request body phải là JSON hoặc bị thiếu', 400)

    access_token, refresh_token, error = User.generate_tokens(data)

    if error:
        return error_response(error, 400)
    
    return success_response(data={'access_token': access_token, 'refresh_token': refresh_token}, code=200)

@auth_bp.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    return success_response(data=User.whoami(), code=200)

   


   

